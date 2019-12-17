import pickle

def init_construct(file_name, path, encrypted):
    data = []
    data.append(path)
    data.append(encrypted)
    with open (file_name,'wb') as datafile:
        pick = pickle.Pickler(datafile)
        pick.dump(data)