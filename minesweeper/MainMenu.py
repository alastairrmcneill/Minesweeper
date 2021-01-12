"""
The file for menu items containing the Menu, Button and Slider classes
"""
import pygame

from minesweeper.Constants import BUTTON_FONT, TEXT_FONT, BACKGROUND

class Menu:
    def __init__(self, window, menu_img):
        """
        Init method for the Menu class

        Arguments:
            window {surface} -- Pygame window to draw to
            menu_img {image} -- Background image for the menu
        """
        self.win = window
        self.width = window.get_width()
        self.height = window.get_height()
        self.original_screen = menu_img
        self.screen = menu_img
        self.clock = pygame.time.Clock()
        self.buttons = []
        self.sliders = []
        self.text_boxes = []

    def run(self):
        """
        Run the menu loop

        Returns:
            list[int] -- List of indexes of the sliders on the screen in the menu when it closes
        """
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
        """
        Add a button object to the menu

        Arguments:
            text {string} -- Text to have centered in the button
            rect {tuple} -- (x, y, width, height) Position of the button
            active_colour {tuple} -- (R, G, B) Colour to have the button when mouse over
            inactive_colour {tuple} -- (R, G, B) Colour to have the button when mouse not over
            text_colour {tuple} -- (R, G, B) Colour to have the text in the button
            func {function} -- Function to execute when button clicked
        """
        self.buttons.append(Button(text, rect, active_colour, inactive_colour, text_colour, func))

    def add_slider(self, options, rect, active_colour, inactive_colour, text_colour):
        """
        Add a slider object to the menu

        Arguments:
            options {list[string]} -- List of items to cycle through
            rect {tuple} -- (x, y, width, height) Position of the slider
            active_colour {tuple} -- (R, G, B) Colour to have the slider when mouse over
            inactive_colour {tuple} -- (R, G, B) Colour to have the slider when mouse not over
            text_colour {tuple} -- (R, G, B) Colour to have the text in the slider
        """
        self.sliders.append(Slider(options, rect, active_colour, inactive_colour, text_colour))

    def add_text_box(self,text, colour, mid_top):
        """
        Add a Text box object to the menu

        Arguments:
            text {string} -- Text you want to display
            colour {tuple} -- (R, G, B) Colour of the text
            mid_top {tuple} -- (x, y) Position of the center top of the text box
        """
        self.text_boxes.append(Text_Box(text, colour, mid_top))

    def draw(self):
        """
        Draw the menu to the screen
        """
        self.win.fill((255,255,255))

        self.draw_buttons()
        self.draw_sliders()
        self.draw_text_boxes()

        self.win.blit(self.screen, (0,0))
        pygame.display.update()

    def draw_sliders(self):
        """
        Loop through all the sliders and draw them
        """
        for slider in self.sliders:
            slider.draw(self.screen)

    def draw_buttons(self):
        """
        Loop throough all the buttons and draw them
        """
        for button in self.buttons:
            button.draw(self.screen)

    def draw_text_boxes(self):
        """
        Loop through all the buttons and drawm them
        """
        for text_box in self.text_boxes:
            text_box.draw(self.screen)


class Button:
    num_of_buttons = 0
    def __init__(self, text, rect, active_colour, inactive_colour, text_colour, func):
        """
        Init method for the button class

        Arguments:
            text {string} -- Text to have centered in the button
            rect {tuple} -- (x, y, width, height) Position of the button
            active_colour {tuple} -- (R, G, B) Colour to have the button when mouse over
            inactive_colour {tuple} -- (R, G, B) Colour to have the button when mouse not over
            text_colour {tuple} -- (R, G, B) Colour to have the text in the button
            func {function} -- Function to execute when button clicked
        """
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
        """
        Function to execute when main menu loop runs. Determines what to do when clicked
        """
        pos = pygame.mouse.get_pos()
        if self.mouse_over(pos):
            self.colour = self.active_colour
            if pygame.mouse.get_pressed()[0] == 1:
                self.func()
                self.done = True
        else:
            self.colour = self.inactive_colour

    def mouse_over(self, pos):
        """
        Check if the mouse is over the button

        Arguments:
            pos {tuple} -- (x,y) Position of the mouse on the screen

        Returns:
            boolean -- If the mouse is over the button
        """
        return pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height


    def draw(self, screen):
        """
        Draw the button to the screen

        Arguments:
            screen {surface} -- Pygame surface to draw on to
        """
        pygame.draw.rect(screen, self.colour, self.rect)

        text = BUTTON_FONT.render(self.button_text, True, self.text_colour)
        text_rect = text.get_rect(center = ((self.x + self.width // 2), (self.y + self.height // 2)))
        screen.blit(text, text_rect)
        self.is_highlighted = False

class Slider(Button):
    def __init__(self, options, rect, active_colour, inactive_colour, text_colour):
        """
        Init method for the slider class

        Arguments:
            options {list[string]} -- List of items to cycle through
            rect {tuple} -- (x, y, width, height) Position of the slider
            active_colour {tuple} -- (R, G, B) Colour to have the slider when mouse over
            inactive_colour {tuple} -- (R, G, B) Colour to have the slider when mouse not over
            text_colour {tuple} -- (R, G, B) Colour to have the text in the slider
        """
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
        """
        Function to execute every time the main menu loop runs, determines what to do when clicked
        """
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
        """
        Is the mouse over the left arrow

        Arguments:
            pos {tuple} -- (x,y) Mouse position on screen

        Returns:
            boolean -- Returns if mouse over the left arrow
        """
        return pos[0] > self.left_rect[0] and pos[0] < self.left_rect[0] + self.left_rect[2] and pos[1] > self.left_rect[1] and pos[1] < self.left_rect[1] + self.left_rect[3]

    def mouse_over_right(self, pos):
        """
        Is the mouse over the right arrow

        Arguments:
            pos {tuple} -- (x,y) Mouse position on screen

        Returns:
            boolean -- Returns if mouse over the right arrow
        """
        return pos[0] > self.right_rect[0] and pos[0] < self.right_rect[0] + self.right_rect[2] and pos[1] > self.right_rect[1] and pos[1] < self.right_rect[1] + self.right_rect[3]

    def cycle(self):
        """
        Increment the index of the list and change what is shown on the slider
        """
        self.index = (self.index + 1) % self.len
        self.button_text = self.options[self.index]

    def right(self):
        """
        Increment the index when clicked right arrow
        """
        self.index = (self.index + 1) % self.len
        self.button_text = self.options[self.index]


    def left(self):
        """
        Decrement the index when clicked left arrow
        """
        self.index = (self.index - 1) % self.len
        self.button_text = self.options[self.index]

    def draw_arrows(self, screen):
        """
        Draw the arrows to the screen

        Arguments:
            screen {surface} -- Pygame surface to draw to
        """
        pygame.draw.line(screen, self.right_colour, ((self.x + self.width + self.width // 10 ,self.y + self.height // 5)), (self.x + self.width + self.width // 4 ,self.y + self.height // 2), 5)
        pygame.draw.line(screen, self.right_colour, ((self.x + self.width + self.width // 10 ,self.y + self.height - self.height // 5)), (self.x + self.width + self.width // 4 ,self.y + self.height // 2), 5)

        pygame.draw.line(screen, self.left_colour, ((self.x - self.width // 10 ,self.y + self.height // 5)), (self.x - self.width // 4 ,self.y + self.height // 2), 5)
        pygame.draw.line(screen, self.left_colour, ((self.x - self.width // 10 ,self.y +self.height - self.height // 5)), (self.x - self.width // 4 ,self.y + self.height // 2), 5)

    def draw(self, screen):
        """
        Draw the whole slider

        Arguments:
            screen {surface} -- Pygame surface to draw to
        """
        self.draw_arrows(screen)
        super().draw(screen)


class Text_Box:
    def __init__(self, text, colour, mid_top):
        """
        Init method for text box

        Arguments:
            text {string} -- Text to be displayed
            colour {tuple} -- (R, G, B) Colour to display text
            mid_top {tuple} -- (x, y) Mid top point of the text box
        """
        self.text = text
        self.colour = colour
        self.mid_top = mid_top
        self.x = self.mid_top[0]
        self.y = self.mid_top[1]

    def draw(self, screen):
        """
        Draw the text box to the screen

        Arguments:
            screen {surface} -- Pygame surface to draw to
        """
        lines = self.text.splitlines()

        y = self.y

        for line in lines:
            text = TEXT_FONT.render(line, True, self.colour)
            rect = text.get_rect(midtop = (self.x, y))
            pygame.draw.rect(screen, BACKGROUND, rect)
            screen.blit(text, rect)

            y = y + text.get_height() + 5
