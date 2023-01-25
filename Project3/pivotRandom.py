import random


def quick_sort_pivot_random(arr, low, high):

    if high > low:
        position = rearrange(arr, low, high)
        quick_sort_pivot_random(arr, low, position - 1)
        quick_sort_pivot_random(arr, position + 1, high)


def rearrange(arr, low, high):

    pindex = random.randint(low, high)
    arr[pindex], arr[high] = arr[high], arr[pindex]

    pivot = arr[high]

    index = low - 1
    for i in range(low, high):
        if arr[i] < pivot:
            index += 1
            arr[i], arr[index] = arr[index], arr[i]

    position = index + 1
    arr[high] = arr[position]
    arr[position] = pivot
    return position
