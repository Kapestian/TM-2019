import pickle

def init_construct(file_name, path, encrypted=False):
    data = []
    data.append(path)
    data.append(encrypted)
    with open (file_name[:-4],'wb') as datafile:
        pick = pickle.Pickler(datafile)
        pick.dump(data)

init_construct('supermuscs.msg','SuperMuscs.png')
init_construct('confirmation.msg','confirmation.png')
init_construct('demain.msg','demain.png')