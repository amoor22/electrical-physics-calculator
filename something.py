from pyperclip import copy
long = 43
string = ''
for i in range(1, long + 1):
    print('ه' * i)
    string += 'ه' * i + '\n'
for i in range(long, 0, -1):
    string += 'ه' * i + '\n'
    print('ه' * i)
copy(string)