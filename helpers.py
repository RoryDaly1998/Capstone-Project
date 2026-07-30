def is_sequence(list, sequence_length):
    '''Finds sequences of consecutive integers in a list of given length.'''
    sorted_list = sorted(list)

    while (i + (sequence_length - 1)) <= len(list):
        if sorted_list[i + (sequence_length - 1)] - sorted_list[i] == sequence_length - 1:
            return True
        else:
            i += 1

    return False