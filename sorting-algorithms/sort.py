#WAYPOINT01: Algorithm Performance Measurement
def calculate_algorithm_cost(algorithm_stats, operation_costs):
    """
    Calculate sorting algorithm's execution cost 
    
    parameter:
    ----------------------
    algorithm_stats: operations performed by the sort function
        tuple (comparisons, reads, writes)
            comparisons: Number of comparison operations
                integer
            reads: Number of read access operations 
                integer
            writes: Number of write access operations
                integer
    operation_costs
        tuple (comparison_cost, read_cost, write_cost)
            comparison_cost: the cost of performing a comparison
                integer
            read_cost: the cost of performing a read access from the list
                integer
            write_cost: the cost of performing a write access to the list
                integer
    return:
    ----------------------
    the total cost of the algorithm's execution
        integer
    """ 

    (comparisons, reads, writes) = algorithm_stats
    (comparison_cost, read_cost, write_cost) = operation_costs
    return (comparisons * comparison_cost) + (reads * read_cost) + (writes * write_cost)

# WAYPOINT02: Bubble Sort
def bubble_sort(l):
    """
    Sort the input list's elements by their ascending order.
    Method: bubble sort
    Parameter:
    --------------------
    l
        list
    Return:
    ---------------------
    (c, r, w) 
        tuple 
        c: Number of comparison operations
        r: Number of read access operations (to the list of elements)
        w: Number of write access operations (to the list of elements)    
    """
    # Raise value
    if not isinstance(l, list):
        raise TypeError("Not a list")
    
    # Initialize variables to count
    r = c = w = 0
    lenL = len(l)
    swapped = True 

    # only if there isn't any swap will the loop stop 
    while swapped:
        swapped = False   

        for i in range(1, lenL):
            r += 2
            c += 1 
            if l[i - 1] > l[i]:
                # Swap the elements
                l[i - 1], l[i] = l[i], l[i - 1]
                w += 2
                swapped = True # loop again  
        lenL -= 1  
    
    return c, r, w 

# WAYPOINT03: Selection Sort
def selection_sort(l):

    """
    Sort the input list's elements by their ascending order.
    Method: Insertion sort
    Parameter:
    --------------------
    l: list type
 
    Return:
    ---------------------
    (c, r, w) 
        tuple 
        c: Number of comparison operations
        r: Number of read access operations (to the list of elements)
        w: Number of write access operations (to the list of elements)    
    """
    # Raise value
    if not isinstance(l, list):
        raise TypeError("Not a list")
    
    # Initialize variables to count
    r = c = w = 0

    for i in range(len(l)):
        # Assign the smallest to the first item of the unsorted segment
        index_temp_min_value = i 
        # Loop iterates over the unsorted items
        for j in range(i + 1, len(l)):
            c += 1  
            r += 2                          
            if l[j] < l[index_temp_min_value]:
                index_temp_min_value = j 
                                   
        c += 1
        if index_temp_min_value != i:
            # swap values of the lowest unsorted ele with the first unsorted ele 
            l[i], l[index_temp_min_value] = l[index_temp_min_value], l[i]
            w += 2
            r += 2

    return c, r, w 

#WAYPOINT4: Insertion Sort 
def insertion_sort(l):  
    """
    Sort the input list's elements by their ascending order.
    Method: Insersion sort
    Parameter:
    --------------------
    l: list type
 
    Return:
    ---------------------
    (c, r, w) 
        tuple 
        c: Number of comparison operations
        r: Number of read access operations (to the list of elements)
        w: Number of write access operations (to the list of elements)    
    
    """
    # Raise value
    if not isinstance(l, list):
        raise TypeError("Not a list")
    
    # Initialize variables to count
    r = c = w = 0   
    i = 1  # start with 2nd element
    c += 1 
    while i < len(l):
        j = i # sellect current element 
        # comparation current element with all elements in the left side  
        c += 2
        r += 2
        while j > 0 and l[j - 1] > l[j]:   
            # Swap other elements to the right to create the correct position 
            # and shift the unsorted element
            l[j - 1], l[j] = l[j], l[j - 1]       
            w += 2   
            j -= 1 
        i += 1 # increment current element index
            
    return c, r, w

#WAYPOINT5: Merge Sort
def merge_sort(l):  
    """
    Sort the input list's elements by their ascending order.
    Method: Merge sort
    Parameter:
    --------------------
    l: list type
 
    Return:
    ---------------------
    (c, r, w) 
        tuple 
        c: Number of comparison operations
        r: Number of read access operations (to the list of elements)
        w: Number of write access operations (to the list of elements)    
    
    """    
    # Raise value
    if not isinstance(l, list):
        raise TypeError("Not a list")

    # Initialize variables to count
    c = r = w = 0

    def merge_sort_aux(l, start1, last2):
        """
        Split the list to sublist till size becomes one by recursively calls itself 
        and merge them
        
        Parameter
        -------------------
        start1: the first index of the list in need of splitting
            int
        last2: the last index of the list in need of splitting
            int
        """
        nonlocal c, w, r

        def merge(l, s1, l1, s2, l2):    
            """
            Sort the sublists and merge two halves
            
            Parameter
            ----------------------
            l: unsorted list
                list
            s1: the index of the first element of the 1st list (left side)
                int  
            l1: the index of the last element of the 1st list (left side)
                int
            s2: the index of the first element of the 2nd list (right side)
                int
            l2: the index of the last element of the 2nd list (right side)
                int
            """
            nonlocal c, r, w

            # Create temporary list to store sorted value
            tempList = l.copy() 

            # Compare pairs of values of two list, start from the first element
            i = s1 # Beginning of the left list
            j = s2 # Beginning of the right list
            k = 0

            # Compare and add to temporary list
            c += 2
            while i <= l1 and j <= l2: 
                c += 3
                r += 2 
                w += 1    
                if l[i] < l[j]:
                    tempList[k] = l[i]
                    i = i + 1
                    k = k + 1                   
                else:
                    tempList[k] = l[j]
                    j = j + 1
                    k = k + 1

            # Copy remaining elements of the first list
            c += 1
            while i <= l1:
                tempList[k] = l[i]
                i = i + 1
                k = k + 1
                c += 1
                r += 1
                w += 1

            # Copy remaining elements of the second list            
            c += 1
            while j <= l2:
                tempList[k] = l[j]
                j = j + 1
                k = k + 1
                c += 1
                r += 1
                w += 1

            # Copy elements from tempList to list l
            i = s1
            j = 0          
            c += 1
            while i <= l2:
                l[i] = tempList[j]
                i = i + 1
                j = j + 1
                c += 1
                w += 1     
                r += 1   
      
        # Split the list to sublist untill size become one
        c += 1
        if start1 < last2:
            last1 = (start1 + last2) // 2 
            start2 = last1 + 1
            merge_sort_aux(l, start1, last1) #the left side
            merge_sort_aux(l, start2, last2) #the right side
            # Call merge function to merge subarrays 
            merge(l, start1, last1, start2, last2)
    
    start = 0
    last = len(l)  - 1
    merge_sort_aux(l, start, last) 
     
    return c, r, w

#WAYPOINT 6: Quicksort (Lumo Partition Scheme)
def quicksort_lumo(l):
    """
    Sort the input list's elements by their ascending order.
    Method: Quicksort (Lumo Partition Scheme)
    Parameter:
    --------------------
    l: list type
    Return:
    ---------------------
    (c, r, w)
        tuple
        c: Number of comparison operations
        r: Number of read access operations (to the list of elements)
        w: Number of write access operations (to the list of elements)
    """
    # Raise value
    if not isinstance(l, list):
        raise TypeError("Not a list")

    # Initialize variables to count
    c = r = w = 0

    def quicksort(l, left, right):
        nonlocal c, r, w
        def partition(l, left, right):
            """
            Return partition index in order to places the pivot element 
            at its correct position next recursion and places all smaller 
            (smaller than pivot) to left of pivot and all greater elements 
            to right of pivot 
            Method: Take last index as pivot
            Parameter
            ----------------------------
            l
                list
            left: the first index of the left of pivot
                int
            right: the first index of the right of pivot
            
            Return
            ------------------------------
            divider
                int
            """
            nonlocal c, r, w
            # take last index as pivot (item's index using to compare)
            pivot = right
            divider = left

            for i in range(left, right):
                c += 1
                r += 2
                if l[i] < l[pivot]:  #If current element is smaller than pivot, swap them
                    l[i], l[divider] = l[divider], l[i]
                    divider += 1 # increment index of smaller elem
                    w += 2
            l[pivot], l[divider] = l[divider],  l[pivot]
            w += 2
            r += 2

            return divider

        c += 1
        if left < right:
            p = partition(l, left, right) # partition index
            # Separately sort elements before partition and after partition
            quicksort(l, left, p - 1)
            quicksort(l, p + 1, right)

    quicksort(l, 0, len(l) - 1)
    return c, r, w


#WAYPOINT 7: Quicksort (Hoare Partition Scheme)
def quicksort_hoare(l):
    """
    Sort the input list's elements by their ascending order.
    Method: Quicksort (Hoare Partition Scheme)
    Parameter:
    --------------------
    l: list type
    Return:
    ---------------------
    (c, r, w)
        tuple
        c: Number of comparison operations
        r: Number of read access operations (to the list of elements)
        w: Number of write access operations (to the list of elements)
    """
    # Raise value
    if not isinstance(l, list):
        raise TypeError("Not a list")

    # Initialize variables to count
    c = r = w = 0
    
    def quicksort_aux(l, left, right):
  
        nonlocal c, r, w
        def partition(l, left, right):
            """
            Return partition index in order to places the pivot element 
            at its correct position next recursion and places all smaller 
            (smaller than pivot) to left of pivot and all greater elements 
            to right of pivot 
            Method: Take middle index as pivot
            Parameter
            ----------------------------
            l
                list
            left: the first index of the left of pivot
                int
            right: the first index of the right of pivot
            """   
            nonlocal c, r, w
            
             # take middle index as pivot (item's index using to compare)
            pivot = left + (right - left) // 2
            i = left - 1
            j = right + 1
            
            c += 1
            while True:
                # Check elements on the left pivot side
                i += 1
                while l[i] < l[pivot]:
                    i += 1
                    r += 2
                    c += 1

                # Check elements on the right pivot side
                j -= 1
                while l[j] > l[pivot]:
                    j -= 1
                    r += 2
                    c += 1
                c += 1

                if i >= j:
                    return j
                # Only if an element at i (on the left of the pivot) is larger than the
                # element at j (on right right of the pivot), swap them
                l[i], l[j] = l[j], l[i]
                w += 2
                r += 2

        c += 1
        if left < right: # Recursion until there's one element in sublist
            #The index after the pivot, where our lists are split
            p = partition(l, left, right)
            # The left patition which have elememts smaller than pivot value
            quicksort_aux(l, left, p)
            # The right patition which have elememts greater than pivot value
            quicksort_aux(l, p + 1, right)

    quicksort_aux(l, 0, len(l) - 1 )
    return c, r, w

if __name__ == "__main__":

    # TEST CASES FOR WAYPOINT01
    algorithm_stats = (15, 30, 18)
    operation_costs = (2, 3, 5)
    print(calculate_algorithm_cost(algorithm_stats, operation_costs))
    pass

    # TEST CASES FOR WAYPOIN02
    lstBubbleSort01 = [5, 2, 4, 6, 1, 3]
    print("Bubble sort", bubble_sort(lstBubbleSort01))
    pass

    # TEST CASES FOR WAYPOIN03
    lstSelectionSort01 = [5, 2, 4, 6, 1, 3]
    print("Selection Sort:", selection_sort(lstSelectionSort01))
    pass

    # TEST CASES FOR WAYPOIN04
    lstInsertionSort01 = [5, 2, 4, 6, 1, 3]
    print("Insertion Sort : ", insertion_sort(lstInsertionSort01))
    pass

    # TEST CASES FOR WAYPOIN05
    lstMergeSort01 = [5, 2, 4, 6, 1, 3]
    print("Merge Sort : ", merge_sort(lstMergeSort01))

    # TEST CASES FOR WAYPOIN06
    lstQuickLumoSort01 = [5, 2, 4, 6, 1, 3]
    print("Quick Sort Lumo : ", quicksort_lumo(lstQuickLumoSort01))

    # TEST CASES FOR WAYPOIN07
    lstQuickHoareSort01 = [5, 2, 4, 6, 1, 3]
    print("Quick Sort Hoare : ", quicksort_hoare(lstQuickHoareSort01))
