# Install all the tools.
import bisect


# Define the element finding procedure in a list(in order).
def value_in_list(list_input, value_input):
    if value_input <= list_input[0]:
        index_id = 0
    elif value_input > list_input[len(list_input) - 1]:
        index_id = len(list_input) - 1
    else:
        index_id = bisect.bisect_left(list_input, value_input)
        before = list_input[index_id - 1]
        after = list_input[index_id]
        if abs(value_input - after) < abs(value_input - before):
            index_id = index_id
        else:
            index_id = index_id - 1
    return index_id


if __name__ == '__main__':
    num_list = [1, 2, 3, 4, 5, 6, 9, 20, 30, 60]
    print(value_in_list(num_list, 36))