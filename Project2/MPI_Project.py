#Student Name: Emre Sin
#Student Number: 2019400207
#Compile Status: Compiling
#Program Status: Working
#Notes:

from mpi4py import MPI
import sys, getopt

comm = MPI.COMM_WORLD

rank = comm.Get_rank()
size = comm.Get_size()

argv = sys.argv[1:]
inputf = ""
testf = ""
merge_method = ""


# getting arguments from the command line
arguments, values = getopt.getopt(
    #it makes it possible to give shortened version of the arguments such as -i -t -o 
    argv, ["i:t:o:"], ["input_file=", "test_file=", "merge_method="]
)
for arg, val in arguments:

    if arg == "--input_file":
        inputf = val

    elif arg == "--test_file":
        testf = val

    elif arg == "--merge_method":
        merge_method = val


#splitting unigrams here
def unigram_splitter(text):
    splitted = text.split(" ")
    return splitted

#splitting bigrams here
def bigram_splitter(text):
    splitted = text.split()
    output = []
    index = 0
    for word in splitted[:-1]:
        output.append(f"{word} {splitted[index+1]}")
        index += 1
    return output

#this function distributes the load evenly and returns a dictionary that holds tasks of every worker
def task_distributor(tasks, num_worker):
    #check if there is excess of workers 
    if num_worker > len(tasks):
        output = {}
        copy_tasks = tasks.copy()
        for i in range(1, len(tasks) + 1):
            output[int(i)] = copy_tasks[:1]
            copy_tasks = copy_tasks[1:]
        for i in range(len(tasks) + 1, num_worker + 1):
            output[int(i)] = []
        return output
    num_tasks = len(tasks)
    base_tasks_by_worker = int(num_tasks / num_worker)
    mod = num_tasks % num_worker
    output = {}
    copy_tasks = tasks.copy()

    for i in range(1, num_worker + 1):
        temp = 1 if mod > 0 else 0
        output[int(i)] = copy_tasks[: base_tasks_by_worker + temp]
        copy_tasks = copy_tasks[base_tasks_by_worker + temp :]
        if mod != 0:
            mod -= 1
    return output

#check merge_method argument to decide how to merge
if merge_method == "MASTER":
    #check if it is master process or not
    if rank == 0:

        #get the input text to an array line by line splitted by </s>
        with open(inputf) as f:
            arr = f.read()
        lines = arr.split("</s>")

        #stripping every line and adding </s> back
        for a in range(len(lines)):
            text = lines[a].strip() + " </s>"
            lines[a] = text

        #distribution of the tasks to workers evenly
        NUM_WORKER = size - 1
        distribution = task_distributor(lines, NUM_WORKER)

        for i in range(1, NUM_WORKER + 1):
            tasks = distribution.get(int(i))
            rank_to_send = int(i)
            comm.send(tasks, rank_to_send)

        #initializing the variables that holds the results
        all_unigram_data = {}
        all_bigram_data = {}

        for i in range(1, NUM_WORKER + 1):
            #get the results of the calculations from the workers
            process_data = comm.recv(source=int(i))


            #merge every workers data 
            if process_data.get("unigram_counts"):
                unigram_counts = process_data.get("unigram_counts")
                
                for unigram in unigram_counts: 
                    if unigram in all_unigram_data:
                        all_unigram_data[unigram] += unigram_counts[unigram]
                    else:
                        all_unigram_data[unigram] = unigram_counts[unigram]
            if process_data.get("bigram_counts"):
                bigram_counts = process_data.get("bigram_counts")
                for bigram in bigram_counts:
                    if bigram in all_bigram_data:
                        all_bigram_data[bigram] += bigram_counts[bigram]
                    else:
                        all_bigram_data[bigram] = bigram_counts[bigram]

            

        output_data = all_bigram_data
        freqs = dict()
        #read the test inputs file
        with open(testf) as f:
            arr = f.readlines()

        for i in range(len(arr)):
            arr[i] = arr[i].strip()

        #calculate the frequencies for the inputs in the test file
        for keys in arr:
            bigram_count = all_bigram_data[keys]
            first_word = keys.split()[0]
            unigram_count = all_unigram_data[first_word]
            freq = bigram_count / unigram_count
            freqs[keys] = freq
            print(keys + ": " + str(freq))

    else:
        #this block executes if the process is worker process

        # receive the task from the master
        tasks = comm.recv(source=0)

        
        print(f"Rank: {rank}, Num Sentences: {len(tasks)}")
        unigram_counts = {}
        bigram_counts = {}

        #loop every sentence in tasks
        for sentence in tasks:
            #find the unigrams and the bigrams
            unigram = unigram_splitter(sentence)
            bigram = bigram_splitter(sentence)

            #adding bigrams and unigrams data to the result dictionary
            for word in unigram:
                if word in unigram_counts:
                    unigram_counts[word] += 1
                else:
                    unigram_counts[word] = 1
            for bigram_word in bigram:
                if bigram_word in bigram_counts:
                    bigram_counts[bigram_word] += 1
                else:
                    bigram_counts[bigram_word] = 1
        #send the result to the master
        comm.send(
            {"unigram_counts": unigram_counts, "bigram_counts": bigram_counts}, dest=0
        )

else:
    #this block will be executed if merge-in-workers method is selected

    if rank == 0:
        # if it is the master process

        #read the sentences from the input file
        with open(inputf) as f:
            arr = f.read()

        lines = arr.split("</s>")

        for a in range(len(lines)):
            text = lines[a].strip() + " </s>"
            lines[a] = text

        #distribute the tasks evenly
        NUM_WORKER = size - 1
        distribution = task_distributor(lines, NUM_WORKER)

        #send the tasks to the workers
        for i in range(1, NUM_WORKER + 1):
            tasks = distribution.get(int(i))
            rank_to_send = int(i)
            comm.send(tasks, rank_to_send)
        
        #receive results from the worker with the highest rank
        output_data = comm.recv(source=size - 1)

        all_bigram_data = output_data["bigram_counts"]
        all_unigram_data = output_data["unigram_counts"]

        #read the testing bigram inputs
        with open(testf) as f:
            arr = f.readlines()

        for i in range(len(arr)):
            arr[i] = arr[i].strip()

        freqs = dict()
        #calculate the frequencies for the inputs given in the test file
        for keys in arr:
            bigram_count = all_bigram_data[keys]
            first_word = keys.split()[0]
            unigram_count = all_unigram_data[first_word]
            freq = bigram_count / unigram_count
            freqs[keys] = freq
            print(keys + ": " + str(freq))

    else:
        #this block runs if it is a worker process

        #receive the task from the master
        tasks = comm.recv(source=0)

        print(f"Rank: {rank}, Num Sentences: {len(tasks)}")
        unigram_counts = {}
        bigram_counts = {}
        #loop every sentence in the tasks and make the calculations
        for sentence in tasks:
            unigram = unigram_splitter(sentence)
            bigram = bigram_splitter(sentence)

            #add the results obtained from the every sentence to the result dictionary
            for word in unigram:
                if word in unigram_counts:
                    unigram_counts[word] += 1
                else:
                    unigram_counts[word] = 1
            for bigram_word in bigram:
                if bigram_word in bigram_counts:
                    bigram_counts[bigram_word] += 1
                else:
                    bigram_counts[bigram_word] = 1

        #take the output from previous worker if it not the first worker otherwise initialize the empty dictionaries
        if rank != 1:
            processed_data = comm.recv(source=rank - 1)
        else:
            processed_data = {"unigram_counts": {}, "bigram_counts": dict()}


        #merge the result of the previous workers calculations with the current calculations
        processed_unigram_data = processed_data["unigram_counts"]
        for key in unigram_counts:
            if key in processed_unigram_data:
                processed_unigram_data[key] += unigram_counts[key]
            else:
                processed_unigram_data[key] = unigram_counts[key]

        processed_bigram_data = processed_data["bigram_counts"]
        for key in bigram_counts:
            if key in processed_bigram_data:
                processed_bigram_data[key] += bigram_counts[key]
            else:
                processed_bigram_data[key] = bigram_counts[key]

        #if it is the last worker then send it to the master otherwise send it to the next worker
        if rank != size - 1:

            comm.send(
                {
                    "unigram_counts": processed_unigram_data,
                    "bigram_counts": processed_bigram_data,
                },
                dest=rank + 1,
            )
        else:
            comm.send(
                {
                    "unigram_counts": processed_unigram_data,
                    "bigram_counts": processed_bigram_data,
                },
                dest=0,
            )
