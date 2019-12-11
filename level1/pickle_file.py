import pickle

def init_construct(file_name, file_type, content, encrypted):
    data = []
    data.append(file_type)
    data.append(content)
    data.append(encrypted)
    with open (file_name,'wb') as datafile:
        pick = pickle.Pickler(datafile)
        pick.dump(data)

init_construct('file1', 'txtfile', 'Hello World', False)
init_construct('file2', 'pngfile', 'file2.png', False)
init_construct('file3', 'txtfile', 'file3.txt', True)