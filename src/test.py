data = [
    2, -10, 3, 15, 7, -1, -6, 10, 7, -4, 2, 9, 1, 0, -5, 0, 9, -2, -5, 1, 10
]
# n = 28
n = 2
result = []
desired_output = [3, 15, 7, -1, -6, 10]


def get_min_len(data, n):
    data1 = data[:]
    data1.sort()
    orig_pos = len(data1)-1
    pos = orig_pos
    total = 0
    while total < n:
        total += data1[pos]
        pos -= 1
    return orig_pos - pos


def get_min_sets(data, n):
    min_set_size = 999999
    min_set_possible = get_min_len(data, n)

    for start_pos in range(len(data) - min_set_possible):
        for end_pos in range(start_pos, len(data)-1):
            total = sum(data[start_pos:end_pos+1])
            set_size = end_pos + 1 - start_pos
            # if size of a set is less then min_size of a saved set then this
            # set is a new minimal set
            if set_size > min_set_size:
                break
            elif total >= n:
                if set_size < min_set_size:
                    # the size of the set is smaller then we have in result
                    min_set_size = set_size
                    result.clear()
                result.append(data[start_pos:end_pos+1])
                break

    return result


min_sets = get_min_sets(data, n)
print(min_sets)


# result = [
#     [row1, row2, row3], [row8, row9, row10]
# ]