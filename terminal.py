
import os
import pickle
import time

class Terminal():

    def __init__(self, folder='level1'):
        self.root = os.getcwd()
        self.cwd = '' #curent working directory
        self.cwd_level = 0 # +1 for every further directories
        self.subdirs = None #avaible child directories
        self.lsfiles = None #avaible files
        self.game_lvl = folder #curent level
        self.deletable_files = ['file1.txt']
        self.deleted_files = []
        self.display = []
        self.prev_display = []
        self.next_display = []
        self.helpcmd =[
            'ls\t Display a list of a directory\'s files and subdirectories',
            'cd\t Change the current directory (ex: cd folder)',
            'cd..\t Go to the parent directory',
            'open \t Open specified file (ex: open file.txt)' ,
            'access\t Connect to another device (ex: access device,password)',
            'del\t Delete specified file (ex: del file.txt)',
            'clue\t Show level\'s clue' ,
            'answer\t Show level\'s answer',]

        # ces données seront "encryptées" avec un pickle
        self.clues = {'level1':'this is a clue', 'level2': 'this is another clue'}
        self.answers = {'level1':'the password is "pswrd"', 'level2': 'this is another answer'}
        self.devices = {'172.685': ('pswrd', 'level2')}

        os.chdir(folder)
        print(f'Terminal starting folder <{folder}>')
        self.init_dir()

    def init_dir(self):
        dir_data = []
        '''inits the directory datas'''

        with open('folder_init','rb') as data:
            dir_data = []
            data_recover = pickle.Unpickler(data)
            dir_data = data_recover.load()

        self.cwd = dir_data[0]
        self.subdirs = dir_data[1]
        self.lsfiles = dir_data[2]
        self.display_print(self.cwd, False)
        print(f'{self.cwd}, sub-directories: {self.subdirs}, sub-files: {self.lsfiles}')

    def simulate(self):
        while True:
            line = input('>> ')
            self.execute_cmd(line)


    def execute_cmd(self, cmd_str): 
        ''' read à terminal line (path:\> action argument) and execute an action'''

        cmd_lst = cmd_str.split(' ')
        action = cmd_lst[0]
        try:
            arg = cmd_lst[1]
        except:
            arg = None

        if action == 'cd':
            self.change_dir(arg)
        elif action == 'cd..':
            self.previous_dir()
        elif action == 'ls':
            self.list_files()
        elif action == 'open':
            self.open_file(arg)
        elif action == 'access':
            arg2 = arg.split(',')
            target = arg2[0]
            password = arg2[1]
            self.access(target, password)
        elif action == 'del':
            self.del_file(arg)
        elif action == 'clue':
            self.get_clue()
        elif action == 'answer':
            self.get_answer()
        elif action == 'cwd':
            self.get_cwd() #debug only
        elif action == 'help':
            self.help_cmd()
        else:
            self.display_print('unable to execute this command')
            print('unable to execute this command')

    def display_print(self, text='', newline=True):
        if len(self.display) < 5: #not full window
            self.display.append(text)
            if newline:
                self.display.append(self.cwd)

        else: #full window
            stored = self.display.pop(0)
            self.display.append(text)
            self.prev_display.append(stored)
            if newline:
                stored = self.display.pop(0)
                self.display.append(self.cwd + ' ')
                self.prev_display.append(stored)
    
    def change_dir(self, newdir): #ajouter ligne curdir
        if self.subdirs != None and newdir in self.subdirs:
            self.cwd_level += 1
            os.chdir(newdir)
            self.init_dir()
        else:
            self.display_print('directory does not exist')
            print('directory does not exist')

    def previous_dir(self): #ajouter ligne curdir
        if self.cwd_level > 0:
            self.cwd_level -= 1
            os.chdir('..')
            self.init_dir()

    def get_cwd(self): #debug only
        print(self.cwd)

    def list_files(self): #blit chaque ligne
        if self.lsfiles != None:
            for directory in self.subdirs:
                dir_str = '<dir>\t{}'.format(directory)
                self.display_print(dir_str)
                print('<dir>', directory, sep='\t')

            for file in self.lsfiles:
                if file not in self.deleted_files:
                    file_str = '<file>\t{}'.format(file)
                    self.display_print(file_str)
                    print('<file>', file, sep='\t')

        else:
            self.display_print('This folder is empty')
            print('This folder is empty')

    def open_file(self, file):
        elt_file = file.split('.')
        name = elt_file[0]
        #extension = elt_file[1]

        if file in self.lsfiles and file not in self.deleted_files:
            #reading file datas
            with open(name, 'rb') as openedfile:
                data_recover = pickle.Unpickler(openedfile)
                file_data = data_recover.load()
            datatype = file_data[0]
            content = file_data[1]
            encrypted = file_data[2]

            #display file if not encrypted
            if encrypted:
                self.display_print('this file is encrypted')
                print('this file is encrypted')

            elif datatype == 'txtfile':
                self.display_print(f'text: {content}')
                print(f'text: {content}')

            elif datatype == 'pngfile':
                self.display_print(f'image: {content}') # à modifier
                print(f'image: {content}') # à modifier

            elif datatype == 'msgfile':
                self.display_print(f'e-mail: {content}')# à modifier
                print(f'e-mail: {content}')# à modifier

        else:
            self.display_print('file does not exist')
            print('file does not exist')
        
    def access(self, target,password):
        if target in self.devices.keys():
            if self.devices[target][0] == password:
                os.chdir(self.root)
                terminal2 = Terminal(self.devices[target][1])
                terminal2.simulate()
            else:
                self.display_print('wrong password')
                print('wrong password')
        else:
            self.display_print('target device not found')
            print('target device not found')

    def del_file(self, file):
        if file in self.lsfiles:
            if file in self.deletable_files:
                self.deleted_files.append(file)
            else:
                self.display_print('unable to delete this file')
                print('unable to delete this file')
        else:
            self.display_print('file does not exist')
            print('file does not exist')

    def get_clue(self):
        self.display_print(self.clues[self.game_lvl])
        print(self.clues[self.game_lvl])

    def get_answer(self):
        self.display_print(self.answers[self.game_lvl])
        print(self.answers[self.game_lvl])

    def clear_screen(self):
        self.display, self.prev_display, self.next_display = [],[],[]
        self.display_print(self.cwd)
        print(self.cwd)

    def help_cmd(self):
        for line in self.helpcmd:
            self.display_print(line, False)
            print(line)
        self.simulate()
    def history_up(self):
        if len(self.display) == 5 and len(self.prev_display) != 0:
            x = self.prev_display.pop(-1)
            y = self.display.pop(-1)
            self.display.insert(0,x)
            self.next_display.insert(0,y)

    def history_down(self):
        if len(display) == 5 and len(next_display) != 0:
            x = self.display.pop(0)
            y = self.next_display.pop(0)
            self.prev_display.append(x)
            self.display.append(y)



if __name__ == '__main__':
    terminal = Terminal()
    terminal.simulate()