import random


def quick_sort_pivot_median_of_three(arr, low, high):

    if high > low:
        position = rearrange(arr, low, high)
        quick_sort_pivot_median_of_three(arr, low, position - 1)
        quick_sort_pivot_median_of_three(arr, position + 1, high)


def rearrange(arr, low, high):

    # pick the first, middle, and last elements
    first = arr[low]
    middle = arr[(high - low + 1) // 2]
    last = arr[high]
    p = 0
    pindex =0
    # find the median of these three elements
    if (first <= middle <= last) or (last <= middle <= first):
        p = middle
        pindex = (high - low + 1) // 2
    elif (middle <= first <= last) or (last <= first <= middle):
        p = first
        pindex = low
    else:
        p = last
        pindex = high


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
