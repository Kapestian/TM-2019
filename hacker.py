import pygame
from pygame.locals import *
import os
import time

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
LIGHTBLUE = (58, 110, 165)
LIGHTGRAY = (212,208,200)
DARKRED = (127, 0, 0)
DARKBLUE = (0, 0, 127)
DARKGREEN = (0, 127,0)


text = '''This is a
multi-line
text file.
'''

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
        terminal_icon = Icon(self, 'icons2/terminal.png', pos=(x, y)); y += dy
        terminal_icon.movable = False
        email_button = Button(self, 'icons2/email.png', pos=(x, y), cmd='App.email_win.visible = not App.email_win.visible'); y += dy
        #icon2.movable = False
        decryptor_icon = Icon(self, 'icons2/decrypt.png', pos=(x, y)); y += dy
        decryptor_icon.movable = False

        App.email_win = Icon(self, 'windows/inbox_win.png', pos=(x, y)); y += dy

        Rectangle(self, Rect(0, 660, 1920, 65))

        quit_button = Button(self, "button/shutdown.png", pos=(10, 665), cmd='App.running = False')
        
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
        pygame.display.flip()


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
        if self is App.selected:
            pygame.draw.rect(App.screen, Node.sel_color, self.rect.move(*pos), 3)

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
    def __init__(self, parent, text, pos=(0, 0), fontcolor=BLACK, **options):
        super().__init__(parent, pos)
        self.text = text
        self.pos = pos
        self.fontcolor = fontcolor
        self.fontsize = 36
        self.editable = True
        self.render()
        self.__dict__.update(options)

    def render(self):
        """Create a surface image of the text."""
        self.font = pygame.font.Font(None, self.fontsize)
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos

    def draw(self, pos):
        """Draw the text object."""
        super().draw(pos)
        App.screen.blit(self.img, self.rect.move(pos))

    def do_event(self, event):
        super().do_event(event)
        if self is App.selected and event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == K_RETURN:
                print('Return')
            elif event.key == K_TAB:
                print('Tab')
            else:
                self.text += event.unicode
            self.render()


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
        App.screen.blit(self.img, self.rect.move(pos))

    def do_event(self, event):
        """Handle mouse clicks and key press events."""

        if event.type == MOUSEBUTTONDOWN:
            self.abs_rect = self.rect.move(self.parent.rect.topleft)

            if self.abs_rect.collidepoint(event.pos) and self.selectable:

                App.selected = self
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
    """Create a window object."""
    def __init__(self, parent, title, rect=Rect(100, 100, 300, 200)):
        super().__init__(parent, rect)

        self.title = title
        self.rect = rect
        self.border_color = BLACK
        self.border_width = 3
        self.background_color = WHITE
        self.titlebar_color = DARKBLUE
        self.outlined = False
        
        Text(self, title, fontcolor=WHITE, pos=(10, 10), movable=False, selectable=False, outlined=False)

    def draw(self, pos=(0, 0)):
        """Draw window with title bar."""
        super().draw(pos)
        pygame.draw.rect(App.screen, self.background_color, self.rect, 0)
        pygame.draw.rect(App.screen, self.titlebar_color, (*self.rect.topleft, self.rect.width, 40))
        pygame.draw.rect(App.screen, self.border_color, self.rect, self.border_width)
        for child in self.children:
            child.draw(self.rect.topleft)


if __name__ == '__main__':
    App().run()
