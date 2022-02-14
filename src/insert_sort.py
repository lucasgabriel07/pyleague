def sort(array, cmp):
    for j in range(1, len(array)):
        chave = array[j]
        i = j - 1
        while i >= 0 and cmp(array[i], chave) < 0:
            array[i + 1] = array[i]
            i -= 1
        array[i + 1] = chave
    return array
