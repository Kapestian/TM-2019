import pickle

def init_construct(file_name, path, encrypted):
    data = []
    data.append(path)
    data.append(encrypted)
    with open (file_name[:-4],'wb') as datafile:
        pick = pickle.Pickler(datafile)
        pick.dump(data)
init_construct('pass.png','pass.png', False)