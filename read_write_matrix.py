def read(filename='matrix.txt'):
    matrix = []
    with open(filename) as file:
        for i in file.readlines():
            matrix.append(list(map(int, i[:-1].split(','))))
    return matrix

def write(matrix, filename='matrix.txt'):
    txt = ''
    for row in matrix:
        txt += ','.join(map(str,row)) + '\n'
    with open(filename, 'w') as file:
        file.write(txt)

def see(filename):
    try:
        file = open(filename)
        if file.read() == '':
            return False
        return True
    except FileNotFoundError:
        return False

if __name__ == '__main__':
    # write([[1,2,3,4,5], [11,2,3,4,5], [50,0,6,7,8], [-1,51,6,9,-1]])
    # print(read())
    print(see('cells.txt'))