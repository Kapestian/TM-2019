import pickle

def init_construct(file_name, path, encrypted=False):
    data = []
    data.append(path)
    data.append(encrypted)
    with open (file_name[:-4],'wb') as datafile:
        pick = pickle.Pickler(datafile)
        pick.dump(data)
init_construct('preuve.png','preuve.jpg')