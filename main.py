import pygame


class Display():

    def __init__(self):
        pygame.init()

        # pygame.display.set_caption("Sudoku")
        # self.icon = pygame.image.load(".png")
        # pygame.display.set_icon(self.icon)

        self.width = 720
        self.height = 720
        self.scale = 0.5
        self.screen = pygame.Surface([self.width, self.height])
        self.window = pygame.display.set_mode((int(self.width * self.scale), int(self.height * self.scale)))

        self.clock = pygame.time.Clock()
        self.fps = 60

    def update(self):
        self.clock.tick(self.fps)
        # pygame.display.set_caption("fps: " + str(self.clock.get_fps()))
        pygame.transform.scale(self.screen, (int(self.width * self.scale), int(self.height * self.scale)), self.window)
        pygame.display.update()


class Board():

    def __init__(self):
        self.grid = []
        self.read("input.txt")

    def read(self, file_name):
        input_file = open(file_name, "r")
        self.grid = [[int(num) for num in line.split(" ")] for line in input_file]

    def print(self):
        for i in self.grid:
            for j in i:
                print(j, end=" ")
            print("")

        print("-" * (len(self.grid[0]) * 2 - 1))

    def check_element_in_line(self, element_value, element_line, element_column):
        for i in range(len(self.grid[element_line])):
            if self.grid[element_line][i] == element_value and i != element_column:
                return False
        return True

    def check_element_in_column(self, element_value, element_line, element_column):
        for i in range(len(self.grid)):
            if self.grid[i][element_column] == element_value and i != element_line:
                return False
        return True

    def check_element_in_square(self, element_value, element_line, element_column):
        start_element_line = element_line - element_line % 3
        start_element_column = element_column - element_column % 3

        for i in range(start_element_line, start_element_line + 3):
            for j in range(start_element_column, start_element_column + 3):
                if self.grid[i][j] == element_value and (i != element_line and j != element_column):
                    return False
        return True

    def check_element(self, element_value, element_line, element_column):
        if self.check_element_in_line(element_value, element_line, element_column):
            if self.check_element_in_column(element_value, element_line, element_column):
                if self.check_element_in_square(element_value, element_line, element_column):
                    return True
        return False

    def find_empty(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

    def solve(self):
        find = self.find_empty()
        if not find:
            return True
        else:
            element_line, element_column = find

        for i in range(1, 10):
            if self.check_element(i, element_line, element_column):
                self.grid[element_line][element_column] = i
                if self.solve():
                    return True
                self.grid[element_line][element_column] = 0


display = Display()
board = Board()

running = True
game_state = "play"

while running:

    if game_state == "main_menu":
        pass

    if game_state == "play":

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        display.screen.fill((192, 192, 192))
        display.update()