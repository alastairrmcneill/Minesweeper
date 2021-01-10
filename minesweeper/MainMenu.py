import pygame
pygame.font.init()
FONT = pygame.font.SysFont("Arial BLACK", 20)

class Menu:
    def __init__(self, window, menu_img):
        self.win = window
        self.width = window.get_width()
        self.height = window.get_height()
        self.screen = menu_img
        self.clock = pygame.time.Clock()
        self.buttons = []
        self.sliders = []

    def run(self):
        run = True

        while run:
            self.clock.tick(20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

            for button in self.buttons:
                button.run()
                if button.done:
                    button.done = False
                    indexes = []
                    for slider in self.sliders:
                        indexes.append(slider.index)

                    return indexes


            for slider in self.sliders:
                slider.run()

            self.draw()



    def add_button(self, text, rect, active_colour, inactive_colour, text_colour, func):
        self.buttons.append(Button(text, rect, active_colour, inactive_colour, text_colour, func))

    def add_slider(self, options, rect, active_colour, inactive_colour, text_colour):
        self.sliders.append(Slider(options, rect, active_colour, inactive_colour, text_colour))

    def draw(self):
        self.win.fill((255,255,255))
        self.draw_buttons()
        self.draw_sliders()

        self.win.blit(self.screen, (0,0))
        pygame.display.update()

    def draw_sliders(self):
        for slider in self.sliders:
            slider.draw(self.screen)

    def draw_buttons(self):
        for button in self.buttons:
            button.draw(self.screen)


class Button:
    num_of_buttons = 0
    def __init__(self, text, rect, active_colour, inactive_colour, text_colour, func):
        self.button_text = text
        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2]
        self.height = rect[3]
        self.rect = rect
        self.active_colour = active_colour
        self.inactive_colour = inactive_colour
        self.colour = self.inactive_colour
        self.text_colour = text_colour
        self.func = func
        self.return_value = self.num_of_buttons
        self.done = False
        Button.num_of_buttons += 1

    def run(self):
        pos = pygame.mouse.get_pos()
        if self.mouse_over(pos):
            self.colour = self.active_colour
            if pygame.mouse.get_pressed()[0] == 1:
                self.func()
                self.done = True
        else:
            self.colour = self.inactive_colour

    def mouse_over(self, pos):
        return pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height


    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)

        text = FONT.render(self.button_text, True, self.text_colour)
        text_rect = text.get_rect(center = ((self.x + self.width // 2), (self.y + self.height // 2)))
        screen.blit(text, text_rect)
        self.is_highlighted = False

class Slider(Button):
    def __init__(self, options, rect, active_colour, inactive_colour, text_colour):
        super().__init__(options[0] , rect, active_colour, inactive_colour, text_colour, None)
        self.options = options
        self.index = 0
        self.button_text = self.options[0]
        self.len = len(options)
        self.left_colour = self.inactive_colour
        self.right_colour = self.inactive_colour
        self.left_rect = (self.x - self.width // 4 , self.y + self.height // 5, self.width // 4 - self.width // 10 , (self.height // 2 - self.height // 5) * 2)
        self.right_rect = (self.x + self.width + self.width // 10 , self.y + self.height // 5, self.width // 4 - self.width // 10 , (self.height // 2 - self.height // 5) * 2)
        self.latched = False

    def run(self):
        pos = pygame.mouse.get_pos()

        # Middle button
        if self.mouse_over(pos):
            self.colour = self.active_colour
            if pygame.mouse.get_pressed()[0] == 1:
                if not self.latched:
                    self.latched = True
                    self.cycle()
            else:
                self.latched = False
        else:
            self.colour = self.inactive_colour

        # Left arrow
        if self.mouse_over_left(pos):
            self.left_colour = self.active_colour
            if pygame.mouse.get_pressed()[0] == 1:
                if not self.latched:
                    self.latched = True
                    self.left()
            else:
                self.latched = False
        else:
            self.left_colour = self.inactive_colour


        # Right arrow
        if self.mouse_over_right(pos):
            self.right_colour = self.active_colour
            if pygame.mouse.get_pressed()[0] == 1:
                if not self.latched:
                    self.latched = True
                    self.right()
            else:
                self.latched = False
        else:
            self.right_colour = self.inactive_colour


    def mouse_over_left(self, pos):
        return pos[0] > self.left_rect[0] and pos[0] < self.left_rect[0] + self.left_rect[2] and pos[1] > self.left_rect[1] and pos[1] < self.left_rect[1] + self.left_rect[3]

    def mouse_over_right(self, pos):
        return pos[0] > self.right_rect[0] and pos[0] < self.right_rect[0] + self.right_rect[2] and pos[1] > self.right_rect[1] and pos[1] < self.right_rect[1] + self.right_rect[3]

    def cycle(self):
        self.index = (self.index + 1) % self.len
        self.button_text = self.options[self.index]

    def right(self):
        self.index = (self.index + 1) % self.len
        self.button_text = self.options[self.index]


    def left(self):
        self.index = (self.index - 1) % self.len
        self.button_text = self.options[self.index]

    def draw_arrows(self, screen):
        pygame.draw.line(screen, self.right_colour, ((self.x + self.width + self.width // 10 ,self.y + self.height // 5)), (self.x + self.width + self.width // 4 ,self.y + self.height // 2), 5)
        pygame.draw.line(screen, self.right_colour, ((self.x + self.width + self.width // 10 ,self.y + self.height - self.height // 5)), (self.x + self.width + self.width // 4 ,self.y + self.height // 2), 5)

        pygame.draw.line(screen, self.left_colour, ((self.x - self.width // 10 ,self.y + self.height // 5)), (self.x - self.width // 4 ,self.y + self.height // 2), 5)
        pygame.draw.line(screen, self.left_colour, ((self.x - self.width // 10 ,self.y +self.height - self.height // 5)), (self.x - self.width // 4 ,self.y + self.height // 2), 5)

    def draw(self, screen):
        self.draw_arrows(screen)
        super().draw(screen)
