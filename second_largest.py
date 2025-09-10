

def is_find_second_largest(arr):
    n = len(arr)
    larges_number = float('inf')
    second_larges_number = float('inf')
    for item in range(n):
        if arr[item] < larges_number:
            second_larges_number = larges_number
            larges_number = arr[item]
        elif arr[item] < second_larges_number and arr[item] != larges_number:
            second_larges_number = arr[item]

    return larges_number, second_larges_number


my_arr = [0, 72, 8, 9, 11, -1, 32, 43]
ss = is_find_second_largest(my_arr)
print(ss)