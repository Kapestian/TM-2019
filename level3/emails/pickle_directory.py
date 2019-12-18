import pickle

def init_construct(folder_name, subdirs, lsfiles):
    data = []
    data.append(folder_name)
    data.append(subdirs)
    data.append(lsfiles)
    with open ('folder_init','wb') as datafile:
        pick = pickle.Pickler(datafile)
        pick.dump(data)

init_construct('Z:\\Hug0\\emails>',None, ('sécuritémax.msg',))
