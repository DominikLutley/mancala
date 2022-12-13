from getkey import getkey, keys
from termcolor import colored
from random import randint
from time import sleep
from templates import TUTORIAL,FORMAT
from functions import clear_screen
from constants import SLEEP_TIME

# Defines the main game class, which handles all logic and game loop
class Game:
    # init function which runs when the class is initiated
    def __init__(self):
        # setting of defaults
        self.info_msg = "YOUR TURN"
        self.active_pit = 0
        self.board_state = [[3,3,3,3,3,3,0],[3,3,3,3,3,3,0]]
        self.board_display = [[],[]]
        self.game_over = False
        self.player_turn = True
        self.extra_turn = False
        self.update_board_display()
        # show tutorial and then start the game
        self.draw_tutorial()
        self.loop()

    # it was necessary to clear and draw to the screen twice to overcome a bug
    def draw(self, value):
        for _ in range(2):
            clear_screen()
            print(value)

    def draw_frame(self):
        self.draw(FORMAT.format(**locals()))

    def draw_tutorial(self):
        self.draw(TUTORIAL)
        # wait for the user to press a key before continuing
        getkey()

    # function to be run once player confirms a pit
    def player_move(self):
        pit_idx = self.active_pit
        # 1 if player, 0 if computer
        cur_player = 1 if self.player_turn else 0
        stone_num = self.board_state[cur_player][pit_idx]
        self.board_state[cur_player][pit_idx] = 0
        cur_pit_idx = 0
        # keeps track of if the stones are landing on the players side of the board
        my_side = True

        for stone_iter in range(stone_num):
            cur_pit_idx = stone_iter + pit_idx + 1
            if not self.player_turn:
                cur_pit_idx += 7
            cur_pit_idx = cur_pit_idx % 14
            if cur_pit_idx > 6:
                cur_pit_idx -= 7
                my_side = cur_player == 0
                self.board_state[0][cur_pit_idx] = self.board_state[0][cur_pit_idx] + 1
            else:
                my_side = cur_player == 1
                self.board_state[1][cur_pit_idx] = self.board_state[1][cur_pit_idx] + 1

        # extra turn if last stone lands in ending pit
        if cur_pit_idx == 6:
            self.extra_turn = True
            return

        # capture opponent's stones if last stone lands in an empty pit on own side of board
        if my_side and self.board_state[cur_player][cur_pit_idx] == 1 and self.board_state[(cur_player + 1) % 2][5 - cur_pit_idx] > 0:
            captured = 1 + self.board_state[(cur_player + 1) % 2][5 - cur_pit_idx]
            self.board_state[cur_player][cur_pit_idx] = 0
            self.board_state[(cur_player + 1) % 2][5 - cur_pit_idx] = 0
            self.board_state[cur_player][6] += captured

    # pseudo-random moves for opponent
    def computer_move(self):
        self.player_turn = False
        self.extra_turn = False
        self.info_msg = "Waiting for opponent..."
        self.active_pit = randint(0,5)
        if self.is_active_pit_empty():
            self.cycle_active_pit()
        self.update_board_display()
        self.draw_frame()
        self.player_move()
        self.cycle_active_pit()
        # delay introduced to visually show which stones were moved
        sleep(SLEEP_TIME)
        if self.extra_turn:
            self.computer_move()
            return
        # sets up player's turn
        self.info_msg = "YOUR TURN"
        self.player_turn = True
        self.active_pit = 0
        if self.is_active_pit_empty():
            self.cycle_active_pit()

    def is_active_pit_empty(self):
        player = 1 if self.player_turn else 0
        return self.board_state[player][self.active_pit] == 0

    # board_display should contain strings, always 2 characters wide, board_state holds numbers
    def update_board_display(self, no_color = False):
        player = 1 if self.player_turn else 0
        self.board_display[0] = [str(x).rjust(2) if x != 0 else "  " for x in self.board_state[0]]
        self.board_display[1] = [str(x).rjust(2) if x != 0 else "  " for x in self.board_state[1]]
        # at ending screen, no highlighted cell
        if no_color:
            return
        # color the active pit with either red or blue depending on which player
        color = 'blue' if self.player_turn else 'red'
        self.board_display[player][self.active_pit] = colored(self.board_display[player][self.active_pit], color, attrs=['reverse', 'blink', 'bold'])

    # run when player changes pits, or when the next non-empty pit needs to be found
    def cycle_active_pit(self, reverse = False):
        for i in range(7):
            delta = 1
            if reverse:
                delta = -1
            self.active_pit = (self.active_pit + delta) % 6
            if not self.is_active_pit_empty():
                break
            # if the pit is cycled 6 times, that means there are no stones left on that side of the board and the game is over
            if i >= 6:
                self.game_over = True
                self.collect_stones()
                break

    def collect_stones(self):
        for player in range(2):
            for i in range(6):
                self.board_state[player][6] += self.board_state[player][i]
                self.board_state[player][i] = 0

    def loop(self):
        while self.game_over == False:
            self.draw_frame()

            key = getkey()
            # quit the game
            if key == "q":
                break

            # cycling pits
            if key == keys.RIGHT:
                self.cycle_active_pit()

            if key == keys.LEFT:
                self.cycle_active_pit(reverse = True)

            # confirm move
            if key == keys.ENTER:
                self.player_move()
                self.cycle_active_pit()
                if not self.extra_turn:
                    self.computer_move()
                self.extra_turn = False

            self.update_board_display()

        if not self.game_over:
            clear_screen()
            return

        # check who won
        points_diff = self.board_state[1][6] - self.board_state[0][6]
        if points_diff > 0:
            self.info_msg = "YOU WON!"
        elif points_diff == 0:
            self.info_msg = "TIE!"
        else:
            self.info_msg = "GAME OVER"
        self.update_board_display(no_color=True)
        self.draw_frame()
        # wait for player to quit game
        while getkey() != 'q':
            continue
        clear_screen()

