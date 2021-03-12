import pickle

def read_highscores(path):
    with open(path, 'rb') as f:
        try:
            data = pickle.load(f)
            return data
        except EOFError:
            return list()

def write_highscores(scores, path):
    with open(path, 'wb') as f:
        pickle.dump(scores, f)

def sort(arr):
    n = len(arr)

    for i in range(n-1):
        for j in range(0, n-i-1):
            if arr[j][1] < arr[j+1][1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]

    return arr
