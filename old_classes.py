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
