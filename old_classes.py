class Image(Window):
    """Display an image in a window."""
    def __init__(self, parent, file, pos=(100, 100)):
        super().__init__(parent, file, pos)

        self.title = file
        self.titlebar_color = DARKRED
        self.img = pygame.image.load(file)
        # self.img = pygame.transform.scale(self.img, (80, 80))
        self.rect = self.img.get_rect()
        self.rect.topleft = pos

    def draw(self, pos=(0, 0)):
        super().draw(pos)
        App.screen.blit(self.img, self.rect.move(pos).move(0, 40))

class TextFile(Window):
    """Create a folder object."""
    def __init__(self, parent, name, lines, rect):
        super().__init__(parent, name, rect)

        x, y = 10, 50
        for line in lines.splitlines():
            Text(self, line, pos=(x, y), movable=False, outlined=False)
            y += 30

    def draw(self, img, pos=(0, 0)):
        """Draw window."""
        super().draw(pos)
        
        for child in self.children:
            child.draw(self.rect.topleft)

class Text(Node):
    """Create an editable text object."""
    def __init__(self, parent, text, pos=(0, 0), fontcolor=BLACK, fontsize=24, **options):
        super().__init__(parent, pos)
        self.text = text
        self.pos = pos
        self.fontcolor = fontcolor
        self.fontsize = fontsize
        self.editable = True
        self.render()
        self.__dict__.update(options)

    def render(self):
        """Create a surface image of the text."""
        self.font = pygame.font.SysFont('consolas', self.fontsize)
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos

    def draw(self, pos):
        """Draw the text object."""
        super().draw(pos)
        App.screen.blit(self.img, self.rect.move(pos))

    def do_event(self, event):
        super().do_event(event)
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE and self.editable:
                self.text = self.text[:-1]
            elif event.key == K_KP_ENTER:
                terminal.execute_cmd('main ls')
            elif self.editable:
                self.text += event.unicode
            
            self.render()