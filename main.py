def create_2d_array(m, n):
    arr = []
    for i in range(m):
        interanal_arr = []
        for j in range(n):
            interanal_arr.append(0)
        arr.append(interanal_arr)
    return arr


def transform_2d_into_1d(arr_2d):
    res_arr = []
    raws = len(arr_2d)
    cols = len(arr_2d[0])
    for i in range(raws):
        for j in range(cols):
            res_arr.append(arr_2d[i][j])
    return res_arr


def my_sort_array(arr):
    for i in range(1, len(arr)):
        for j in range(1, len(arr)):
            if arr[j - 1] > arr[j]:
                tmp = arr[j - 1]
                arr[j - 1] = arr[j]
                arr[j] = tmp

    return arr


m = 3
n = 3
arr1 = create_2d_array(m, n)
counter = 9
for i in range(m):
    for j in range(n):
        arr1[i][j] = counter
        counter -= 1
arr2 = transform_2d_into_1d(arr1)
for i in arr2:
    print(i, end=" ")
arr3 = my_sort_array(arr2)
my_sort_array(arr2)
print()
for i in arr2:
    print(i, end=" ")
