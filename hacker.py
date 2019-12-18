import pygame
from pygame.locals import *
import os
import pickle
import time

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
GREEN = (0,255, 0)
BLUE = (0, 0, 234)
LIGHTBLUE = (58, 110, 165)
LIGHTGRAY = (212,208,200)
DARKRED = (127, 0, 0)
DARKBLUE = (0, 0, 127)
DARKGREEN = (0, 127, 0)

root_folder = os.getcwd()+'/'

message1 = 'images/message1.png'

class App:
    """Create the application."""
    screen = None
    selected = None

    def __init__(self):
        pygame.init()
        self.rect = Rect(0, 0, 1280, 720)
        self.background_color = LIGHTBLUE
        self.title = 'Hacker Desktop Environment'
        self.children = []
        self.flags = FULLSCREEN
        self.t0 = time.time()
        App.screen = pygame.display.set_mode(self.rect.size, self.flags)
        pygame.display.set_caption(self.title)

        x, y = 20, 20
        dy = 120
        terminal_icon = Button(self, 'icons2/terminal.png',cmd="App.create_window(self,'Terminal')", pos=(x, y)); y += dy
        terminal_icon.movable = False
        email_icon = Button(self, 'icons2/email.png', cmd="App.create_window(self,'Inbox')", pos=(x, y)); y += dy
        email_icon.movable = False
        decryptor_icon = Icon(self, 'icons2/decrypt.png', pos=(x, y)); y += dy
        Rectangle(self, Rect(0, 660, 1920, 65))
        quit_button = Button(self, "button/shutdown.png", pos=(10, 665), cmd='App.running = False')

        #terminal = Terminal(self,'windows2/terminal_win.png',(20,20))
        #file1 = File(self, 'pngfile', 'test.png', 'images/hacker.jpg')
        #Inbox(self, 'windows2/inbox_win.png', (60, 70))
        
        #debug


    def create_window(self, win, name=None, content=None):
        if win == 'in_File':
            File(self.parent, name, content, pos=(150,100))
        if win == 'File':
            File(self.parent, name, content, pos=(100,50))
        if win == 'Inbox':
            Inbox(self.parent, 'windows2/inbox_win.png', (350,100))
        if win == 'Terminal':
            terminal = Terminal(self.parent,'windows2/terminal_win.png',(150,50))

    def run(self):
        """Run the main event loop."""
        App.running = True
        while App.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    App.running = False

                if event.type == MOUSEBUTTONDOWN:
                    App.selected = None
                for child in self.children:
                    child.do_event(event)

            self.draw()

        pygame.quit()

    def draw(self, pos=(0, 0)):
        """Draw the objects of the main screen."""
        self.screen.fill(self.background_color)
        for child in self.children:
            child.draw(pos)
        pygame.display.update()


class Node: 
    sel_color = GRAY
    """Create a node class for embedded objects."""
    def __init__(self, parent, rect=Rect(20, 60, 200, 100), **options):

        self.parent = parent
        self.parent.children.append(self)
        self.children = []
        self.rect = rect
        self.abs_rect = rect
        self.visible = True
        self.outlined = True
        self.editable = False
        self.movable = True
        self.selectable = True
        self.color = DARKBLUE
        self.time = 0
        self.__dict__.update(options)

        
    def draw(self, pos):
        """Draw the node and its children."""
        if self.visible:
            if self.outlined:
                pygame.draw.rect(App.screen, self.color, self.rect.move(*pos), 1)
            for child in self.children:
                child.draw(self.rect.topleft)
        #if self is App.selected:
            #pygame.draw.rect(App.screen, Node.sel_color, self.rect.move(*pos), 3)

    def do_event(self, event):
        """Handle mouse clicks and key press events."""

        if event.type == MOUSEBUTTONDOWN:
            self.abs_rect = self.rect.move(self.parent.rect.topleft)

            if self.abs_rect.collidepoint(event.pos) and self.selectable:
                
                # place the selected object on the top
                self.parent.children.remove(self)
                self.parent.children.append(self)

                App.selected = self
                self.click_pos = event.pos

                # detect double click
                t = pygame.time.get_ticks()
                if t - self.time < 200:
                    self.double_click()
                self.time = t

                print('clicked in', self)

        for child in self.children:
            child.do_event(event)

        if self is App.selected:
            if event.type == MOUSEMOTION and event.buttons[0] == 1 and self.movable:
               self.rect.move_ip(event.rel)

    def double_click(self):
        print('double-click in', self)

    def __str__(self):
        """Return a string to name the object."""
        return '{} at ({}, {})'.format(self.__class__.__name__, *self.rect.topleft)

class Text(Node):
    """Create an editable text object."""
    def __init__(self, parent, text, pos=(0, 0), fontcolor=BLACK, fontsize=24, bold=False, **options):
        super().__init__(parent, pos)
        self.text = text
        self.pos = pos
        self.fontcolor = fontcolor
        self.fontsize = fontsize
        self.bold = bold
        self.render()
        self.__dict__.update(options)

    def render(self):
        """Create a surface image of the text."""
        self.font = pygame.font.SysFont('consolas', self.fontsize, self.bold)
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos

    def draw(self, pos):
        """Draw the text object."""
        super().draw(pos)
        if self.visible:
            App.screen.blit(self.img, self.rect.move(pos))

class File(Node):
    def __init__(self, parent, name, content, rect=Rect(100, 100, 600, 400), pos=(100,100),**options):
        super().__init__(parent, pos)

        self.outlined = False
        self.movable = True
        self.selectable = True
        self.name = name
        self.content = pygame.image.load(root_folder+content)
        self.rect = self.content.get_rect()
        self.rect.topleft = pos

        Button(self, root_folder+'button/close.png', (self.rect.width-30, -25),'self.parent.hide()')
        print(self.rect)
        self.__dict__.update(options)

    def draw(self, pos=(70,70)):
        """draw file object"""
        for child in self.children[1:]:
            self.children.remove(child)
        super().draw(pos)
        if self.visible:
            pygame.draw.rect(App.screen, LIGHTGRAY, self.rect,0)
            pygame.draw.rect(App.screen, BLUE, (self.rect.topleft[0], self.rect.topleft[1]-30, self.rect.width, 30))
            pygame.draw.rect(App.screen, WHITE, (self.rect.topleft[0]+3, self.rect.topleft[1]+3, self.rect.width-6, self.rect.height-6))
            App.screen.blit(self.content, self.rect.topleft)
            pygame.draw.rect(App.screen, LIGHTGRAY, (self.rect.topleft[0], self.rect.topleft[1]-30, self.rect.width, self.rect.height+30), 3)
            Text(self, self.name, (10,-22),LIGHTGRAY, 18, True, outlined=False, editable=False)

            for child in self.children:
                child.draw(self.rect.topleft)

    def hide(self):
        print('hide', self, self.children)
        self.visible = False
        for child in self.children:
            child.visible = False
        self.editable = False
        self.selectable = False


class Icon(Node):
    def __init__(self, parent, file, pos=(100, 100)):
        super().__init__(parent, pos)

        self.file = file
        self.img = pygame.image.load(file)
        self.rect = self.img.get_rect()
        self.rect.topleft = pos
        self.outlined = False

    def draw(self, pos=(0, 0)):
        super().draw(pos)
        if self.visible:
            App.screen.blit(self.img, self.rect.move(pos))


class Button(Node):
    def __init__(self, parent, file, pos=(100, 100), cmd=''):
        super().__init__(parent, pos)

        self.file = file
        self.img = pygame.image.load(file)
        self.rect = self.img.get_rect()
        self.rect.topleft = pos
        self.outlined = False
        self.movable = False
        self.cmd = cmd

    def draw(self, pos=(0, 0)):
        super().draw(pos)
        if self.visible:
            App.screen.blit(self.img, self.rect.move(pos))

    def do_event(self, event):
        """Handle mouse clicks and key press events."""

        if event.type == MOUSEBUTTONDOWN:
            self.abs_rect = self.rect.move(self.parent.rect.topleft)

            if self.abs_rect.collidepoint(event.pos) and self.selectable:

                App.selected = None
                self.click_pos = event.pos
                exec(self.cmd)

class Rectangle(Node):
    """Create a rectangle object."""
    def __init__(self, parent, rect=Rect(100, 100, 300, 200), **options):
        super().__init__(parent, rect)

        self.rect = rect
        self.border_color = BLACK
        self.border_width = 0
        self.background_color = LIGHTGRAY
        self.outlined = False
        self.selectable = False
        
    def draw(self, pos=(0, 0)):
        """Draw rectangle."""
        super().draw(pos)
        pygame.draw.rect(App.screen, self.background_color, self.rect, 0)
        for child in self.children:
            child.draw(self.rect.topleft)

class Window(Node):
    """create a window object"""
    def __init__(self, parent, image, pos = (30, 30)):
        super().__init__(parent)

        self.frame = pygame.image.load(root_folder+image)
        self.rect = self.frame.get_rect()
        self.rect.topleft = pos
        self.outlined = False

        Button(self, root_folder+'button/close.png', (self.rect.width-30, 7), 'print(self.parent); self.parent.hide()')

    def draw(self, pos=(100, 150)):
        """draw window object"""
        super().draw(pos)
        if self.visible:
            App.screen.blit(self.frame,self.rect.move(pos))
            for child in self.children:
                child.draw(self.rect.topleft)

    def hide(self):
        print('hide', self, self.children)
        self.visible = False
        self.editable = False
        self.selectable = False

        for child in self.children:
            child.visible = False
            child.editable = False
            child.selectable = False


class Terminal(Window):
    """Create a terminal object."""

    def __init__(self, parent, image, pos, level='level2'):
        super().__init__(parent, image, pos)
        os.chdir(root_folder)
        self.editable = True
        self.root_folder = os.getcwd()
        self.cwd = '' #curent working directory 
        self.cwd_level = 0 # +1 for every further directories
        self.subdirs = None #avaible child directories
        self.lsfiles = None #avaible files
        self.game_lvl = level #curent level
        self.deletable_files = ['file1.txt']
        self.deleted_files = []
        self.display = []
        self.display_obj = []
        self.prev_display = []
        self.next_display = []
        self.helpcmd =[
            'ls        Display a list of a directory\'s files and subdirectories',
            'cd        Change the current directory (ex: cd folder)',
            'cd..      Go to the parent directory',
            'open      Open specified file (ex: open file.txt)' ,
            'access    Connect to another device (ex: access device,password)',
            'del       Delete specified file (ex: del file.txt)',
            'clue      Show level\'s clue' ,
            'answer    Show level\'s answer',]

        # ces données seront "encryptées" avec un pickle
        self.clues = {'level1':'"le mot de passe est facile"', 'level2': '','level3':'', 'level4':''}
        self.answers = {'level1':'"la solution est "access 172.685,Jack"', 'level2': '"la solution est "access 182.842,20.12.18""','level3':'"la solution est "access 152.111,ferrari2000""'}
        self.devices = {'172.685': ('Jack', 'level2'),'182.842': ('20.12.18', 'level3'),'152.111': ('ferrari2000', 'level4')}

        os.chdir(level)
        print(f'Terminal starting folder <{level}>')
        self.init_dir()

    def draw(self, pos=(0, 0)):
        """Draw terminal object"""
        super().draw(pos)
        for child in self.children:
            child.draw(self.rect.topleft)
    
    def do_event(self, event):
        super().do_event(event)
        if event.type == KEYDOWN and self.editable == True:
            if event.key == K_CAPSLOCK:        
                self.display_print('test', False)
            elif event.key == K_RETURN:
                self.execute_cmd(self.display[-1])
            elif event.key == K_BACKSPACE:
                if len(self.display[-1]) > len(self.cwd)+1:
                   self.display[-1] = self.display[-1][:-1]
            elif event.key == K_UP:
                self.history_up()
            elif event.key == K_DOWN:
                self.history_down()
            else:
                self.display[-1] += event.unicode
        self.draw_display()

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
        self.display_print(self.cwd+' ', False)
        print(f'{self.cwd}, sub-directories: {self.subdirs}, sub-files: {self.lsfiles}')

    def simulate(self):
        while True:
            line = input('>> ')
            self.execute_cmd(line)


    def execute_cmd(self, cmd_str): 
        ''' read à terminal line (path:\> action argument) and execute an action'''

        cmd_w_path = cmd_str[len(self.cwd)+1:] #format the chaine without the path name
        cmd_lst = cmd_w_path.split(' ')
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
            if arg != None:
                try:
                    arg2 = arg.split(',')
                    target = arg2[0]
                    password = arg2[1]
                    self.access(target, password)
                except:
                    self.display_print('error')
        elif action == 'del':
            self.del_file(arg)
        elif action == 'clue':
            self.get_clue()
        elif action == 'answer':
            self.get_answer()
        elif action == 'cwd':
            self.get_cwd() #debug only
        elif action[:5] =='level':
            self.change_level(action)
        elif action == 'help':
            self.help_cmd()
        elif action == 'cls':
            self.clear_screen()
        elif action == 'exit':
            App.running = False
        else:
            self.display_print('unable to execute this command')
            print('unable to execute this command')

    def display_print(self, text='', newline=True):

        if len(self.display) < 15 : #not full window
            self.display.append(text)
            if newline:
                self.display.append(self.cwd+' ')

        else: #full window
            stored = self.display.pop(0)
            self.display.append(text)
            self.prev_display.append(stored)
            if newline:
                stored = self.display.pop(0)
                self.display.append(self.cwd+' ')
                self.prev_display.append(stored)
        
        self.draw_display()

    def draw_display(self):
        if self.visible:
            dy = 45
            self.children = self.children[:1]
            for line in self.display:
                Text(self, line, (10,dy), WHITE, 22, outlined=False, movable=False)
                dy += 35

    def change_level(self, level):
        os.chdir(root_folder+level)
        self.cwd_level = 0
        self.display_print('Access granted!',False)
        self.init_dir()
        self.game_lvl= level

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
        else:
            self.display_print(self.cwd+' ', False)

    def get_cwd(self): #debug only
        print(self.cwd)

    def list_files(self): #blit chaque ligne
        if self.subdirs != None:
            for directory in self.subdirs:
                dir_str = '<dir>   {}'.format(directory)
                self.display_print(dir_str, False)
                print('<dir>', directory, sep='\t')

        elif self.lsfiles != None:
            for file in self.lsfiles:
                if file not in self.deleted_files:
                    file_str = '<file>  {}'.format(file)
                    self.display_print(file_str, False)
                    print('<file>', file, sep='\t')
        else:
            self.display_print('This folder is empty', False)
            print('This folder is empty')
        self.display_print(self.cwd+' ', False)

    def open_file(self, file):
        elt_file = file.split('.')
        name = elt_file[0]
        #extension = elt_file[1]

        if self.lsfiles != None:
            if file in self.lsfiles and file not in self.deleted_files:
                #reading file datas
                with open(name, 'rb') as openedfile:
                    data_recover = pickle.Unpickler(openedfile)
                    file_data = data_recover.load()
                path = file_data[0]
                encrypted = file_data[1]

                #display file if not encrypted
                if encrypted:
                    self.display_print('this file is encrypted')
                    print('this file is encrypted')

                else:
                    App.create_window(self, 'File', file, os.getcwd()[40:]+'/'+ path)
                    
            else:
                self.display_print('file does not exist')
                print('file does not exist')
        else: self.display_print('file does not exist')

    def access(self, target,password):
        if target in self.devices.keys():
            if self.devices[target][0] == password:
                self.change_level(self.devices[target][1])
            else:
                self.display_print('wrong password')
                print('Access denied!')
        else:
            self.display_print('target device not found')
            print('target device not found')

    def del_file(self, file):
        if self.lsfiles != None and file in self.lsfiles:
            if file in self.deletable_files:
                self.deleted_files.append(file)
                self.display_print('file deleted')
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
        self.display_print(self.cwd+' ', False)
        print(self.cwd)

    def help_cmd(self):
        for line in self.helpcmd:
            self.display_print(line, False)
            print(line)
        self.display_print(self.cwd+' ', False)

    def history_up(self):
        if len(self.display) == 15 and len(self.prev_display) != 0:
            x = self.prev_display.pop(-1)
            y = self.display.pop(-1)
            self.display.insert(0,x)
            self.next_display.insert(0,y)
            self.draw_display()

    def history_down(self):
        if len(self.display) == 15 and len(self.next_display) != 0:
            x = self.display.pop(0)
            y = self.next_display.pop(0)
            self.prev_display.append(x)
            self.display.append(y)
            self.draw_display()
   
class Inbox(Window):
    """Create a mail app object"""

    def __init__(self, parent, image, pos,):
        super().__init__(parent, image, pos)
        
        dy = 100
        Button(self, root_folder+'user_mail\mail1.png', (15, dy), "App.create_window(self.parent,'in_File','Urgent.msg', message1)")
        dy += 70

    def draw(self, pos=(150, 100)):
        """draw inbox object"""
        super().draw(pos)
        for child in self.children:
            child.draw(self.rect.topleft)

if __name__ == '__main__':
    App().run()