"""You want to sort a list of numbers efficiently by taking advantage of parallel processing.
The goal is to:
Divide the list into two halves.
Sort each half simultaneously using threads.
Merge the two sorted halves into a fully sorted list."""

"""Divide and Conquer:
Split the array into two sublists:
First half: arr[0:n//2]
Second half: arr[n//2:n]
Parallel Sorting:
Use two threads (t1 and t2) to sort each half concurrently.
Each thread runs sort_sublist(lst, start, end) which sorts its sublist in-place.
Merging:
After both halves are sorted, use a third thread (t3) to merge the two halves.
The merge function compares elements from both halves and places the smaller element into a new array merged_arr.
Result:
merged_arr contains the fully sorted array.
Parallel sorting improves efficiency for larger arrays by leveraging multiple threads."""

import threading
def sort_sublist(lst, start, end):
    sublist = lst[start:end]
    sublist.sort()
    lst[start:end] = sublist
def merge(lst, start1, end1, start2, end2, merged):
    i, j, k = start1, start2, 0
    while i < end1 and j < end2:
        if lst[i] < lst[j]:
            merged[k] = lst[i]
            i += 1
        else:
            merged[k] = lst[j]
            j += 1
        k += 1
    while i < end1:
        merged[k] = lst[i]
        i += 1
        k += 1
    while j < end2:
        merged[k] = lst[j]
        j += 1
        k += 1
        
arr = [7, 12, 19, 3, 18, 4, 2, 6, 15, 8]
n = len(arr)
merged_arr = [0] * n

# Sorting threads
t1 = threading.Thread(target=sort_sublist, args=(arr, 0, n//2))
t2 = threading.Thread(target=sort_sublist, args=(arr, n//2, n))

t1.start()
t2.start()
t1.join()
t2.join()

# Merging thread
t3 = threading.Thread(target=merge, args=(arr, 0, n//2, n//2, n, merged_arr))
t3.start()
t3.join()

print("Sorted Array:", merged_arr)
