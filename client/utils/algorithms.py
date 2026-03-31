def mergesort(data, key_func, reverse=False):
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left = mergesort(data[:mid], key_func, reverse)
    right = mergesort(data[mid:], key_func, reverse)

    return merge(left, right, key_func, reverse)


def merge(left, right, key_func, reverse):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        left_val = key_func(left[i])
        right_val = key_func(right[j])

        condition = (left_val >= right_val) if reverse else (left_val <= right_val)
        if condition:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result