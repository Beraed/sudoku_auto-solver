import pygame


class Display():

    def __init__(self):
        pygame.init()

        # pygame.display.set_caption("Sudoku")
        # self.icon = pygame.image.load(".png")
        # pygame.display.set_icon(self.icon)

        self.width = 720
        self.height = 800
        self.scale = 1
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
        self.state_grid = []
        self.read("input.txt")

        self.gap = display.width // 9
        self.selected_col = -1
        self.selected_row = -1

    def read(self, file_name):
        input_file = open(file_name, "r")
        self.grid = [[int(num) for num in line.split(" ")] for line in input_file]

        self.state_grid = [[0 for j in range(9)] for i in range(9)]
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 0:
                    self.state_grid[i][j] = "W"
                else:
                    self.state_grid[i][j] = "R"

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

    def draw(self):

        # Draw Selected
        for i in range(9):
            for j in range(9):
                if i == self.selected_row and j == self.selected_col:
                    pygame.draw.rect(display.screen, (255, 200, 200),
                                     pygame.Rect(1 + j * self.gap, 1 + i * self.gap, self.gap - 1, self.gap - 1))

        # Draw Lines

        for i in range(10):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(display.screen, (0, 0, 0), (0, i * self.gap), (display.width, i * self.gap), thick)
            pygame.draw.line(display.screen, (0, 0, 0), (i * self.gap, 0), (i * self.gap, display.height), thick)

        # Draw Numbers

        font = pygame.font.SysFont("arial", self.gap)

        for i in range(9):
            for j in range(9):
                if board.grid[i][j] != 0:
                    if self.state_grid[i][j] == "R":
                        color = (0,0,0)
                    else:
                        color = (128,0,0)

                    text = font.render(str(board.grid[i][j]), True, color)
                    display.screen.blit(text, (self.gap // 4 + j * self.gap, -self.gap // 16 + i * self.gap))

        # Draw Border
        pygame.draw.rect(display.screen, (240, 240, 240),
                         pygame.Rect(0, display.width+1, display.width, display.height - display.width))

    def key_press(self):
        global game_state, event, board

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            mouse_position_x = int(mouse_position[0] * (1 / display.scale))
            mouse_position_y = int(mouse_position[1] * (1 / display.scale))

            if event.button == 1:
                if pygame.Rect(0, 0, display.width, display.width).collidepoint(mouse_position_x, mouse_position_y):
                    self.selected_col = mouse_position_x // self.gap
                    self.selected_row = mouse_position_y // self.gap

                else:
                    self.selected_col = -1
                    self.selected_row = -1

        if event.type == pygame.KEYDOWN:
            if self.selected_col >= 0 and self.selected_col < 9 and self.selected_row >= 0 and self.selected_row < 9:
                if self.state_grid[self.selected_row][self.selected_col] == "W":
                    if event.key == pygame.K_1:
                        self.grid[self.selected_row][self.selected_col] = 1
                    elif event.key == pygame.K_2:
                        self.grid[self.selected_row][self.selected_col] = 2
                    elif event.key == pygame.K_3:
                        self.grid[self.selected_row][self.selected_col] = 3
                    elif event.key == pygame.K_4:
                        self.grid[self.selected_row][self.selected_col] = 4
                    elif event.key == pygame.K_5:
                        self.grid[self.selected_row][self.selected_col] = 5
                    elif event.key == pygame.K_6:
                        self.grid[self.selected_row][self.selected_col] = 6
                    elif event.key == pygame.K_7:
                        self.grid[self.selected_row][self.selected_col] = 7
                    elif event.key == pygame.K_8:
                        self.grid[self.selected_row][self.selected_col] = 8
                    elif event.key == pygame.K_9:
                        self.grid[self.selected_row][self.selected_col] = 9
                    elif event.key == pygame.K_0:
                        self.grid[self.selected_row][self.selected_col] = 0

            if event.key == pygame.K_BACKSPACE:
                for i in range(9):
                    for j in range(9):
                        if self.state_grid[i][j] == "W":
                            self.grid[i][j] = 0

            if event.key == pygame.K_s:
                for i in range(9):
                    for j in range(9):
                        if self.state_grid[i][j] == "W":
                            self.grid[i][j] = 0
                self.solve()

            if self.solve_check():
                game_state = "win"
                self.selected_col = -1
                self.selected_row = -1
                print("win")

    def solve_check(self):
        if not self.find_empty():
            for i in range(9):
                for j in range(9):
                    if self.check_element_in_line(self.grid[i][j],i,j) == False:
                        return False
                    if self.check_element_in_column(self.grid[i][j],i,j) == False:
                        return False
                    if self.grid[i][j] == 0:
                         return False
            return True
        return False


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

            board.key_press()

        display.screen.fill((240, 240, 240))
        board.draw()
        display.update()

    if game_state == "win":

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False