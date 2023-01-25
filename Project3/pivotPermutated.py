import random


def quick_sort_pivot_permutated(arr, low, high):

    if high > low:
        position = rearrange(arr, low, high)
        quick_sort_pivot_permutated(arr, low, position - 1)
        quick_sort_pivot_permutated(arr, position + 1, high)


def rearrange(arr, low, high):


    arr[low], arr[high] = arr[high], arr[low]
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
