from getkey import getkey, keys
from termcolor import colored
import os
from random import randint
from time import sleep

TUTORIAL = """

             ╔════════════════════╗
             ║ WELCOME TO MANCALA ║
             ╚════════════════════╝

There are many variants of Mancala, each with different rules. Here are the rules used in this version:

Basic Concepts:
1. Each player has 6 pits with a number of stones in them
2. Each player has a store, which is located to the right of their pits
3. The player with the most stones in their store at the end of the game wins

Playing the Game:
1. Choose one of 6 pits on your side of the board (bottom)
2. Empty this pit, and deposit the stones one by one into the consecutive pits, going counter-clockwise, including both stores
3. If your last stone lands in an empty pit on your side of the board, you capture that stone and the stones from the opposite pit on your opponent's side. Put the captured stones in your store
4. If your last stone lands in your store, you get an extra turn. This can happen multiple times
5. If either player has no moves, the other player collects the remaining pits on their side of the board and puts them in their store
6. The game ends and the player with more stones in their store is the winner

Press any key to continue...
"""

FORMAT = """
  {self.info_msg}

                       ◀◀◀
    ┏━━━━┯━━━━┯━━━━┯━━━━┯━━━━┯━━━━┯━━━━┯━━━━┓
    ┃    │ {self.board_display[0][5]} │ {self.board_display[0][4]} │ {self.board_display[0][3]} │ {self.board_display[0][2]} │ \
{self.board_display[0][1]} │ {self.board_display[0][0]} │    ┃
    ┃ {self.board_display[0][6]} ├────┼────┼────┼────┼────┼────┤ {self.board_display[1][6]} ┃
    ┃    │ {self.board_display[1][0]} │ {self.board_display[1][1]} │ {self.board_display[1][2]} │ {self.board_display[1][3]} │ \
{self.board_display[1][4]} │ {self.board_display[1][5]} │    ┃
    ┗━━━━┷━━━━┷━━━━┷━━━━┷━━━━┷━━━━┷━━━━┷━━━━┛
                       ▶▶▶


┌──────────────────────────────┐
│ press arrow keys switch pits │
│ press [Enter] to confirm     │
│ press 'q' to quit            │
└──────────────────────────────┘
"""

def clear():
    os.system('clear')

class Game:
    def __init__(self):
        self.info_msg = "YOUR TURN"
        self.active_pit = 0
        self.board_state = [[3,3,3,3,3,3,0],[3,3,3,3,3,3,0]]
        self.board_display = [[],[]]
        self.game_over = False
        self.player_turn = True
        self.extra_turn = False
        self.update_board_display()
        self.draw_tutorial()
        self.loop()

    def draw(self, value):
        for _i in range(2):
            clear()
            print(value)

    def draw_frame(self):
        self.draw(FORMAT.format(**locals()))

    def draw_tutorial(self):
        self.draw(TUTORIAL)
        getkey()

    def make_move(self):
        idx = self.active_pit
        player = 1 if self.player_turn else 0
        stone_num = self.board_state[player][idx]
        self.board_state[player][idx] = 0
        j = 0
        my_side = True
        for i in range(stone_num):
            j = i + idx + 1
            if not self.player_turn:
                j += 7
            j = j % 14
            if j > 6:
                j -= 7
                my_side = player == 0
                self.board_state[0][j] = self.board_state[0][j] + 1
            else:
                my_side = player == 1
                self.board_state[1][j] = self.board_state[1][j] + 1
        if j == 6:
            self.extra_turn = True
            return
        if my_side and self.board_state[player][j] == 1 and self.board_state[(player + 1) % 2][5 - j] > 0:
            captured = 1 + self.board_state[(player + 1) % 2][5 - j]
            self.board_state[player][j] = 0
            self.board_state[(player + 1) % 2][5 - j] = 0
            self.board_state[player][6] += captured

    def computer_move(self):
        self.player_turn = False
        self.extra_turn = False
        self.info_msg = "Waiting for opponent..."
        self.active_pit = randint(0,5)
        if self.active_pit_empty():
            self.cycle_cells()
        self.update_board_display()
        self.draw_frame()
        self.make_move()
        self.cycle_cells()
        sleep(2)
        if self.extra_turn:
            self.computer_move()
            return
        self.info_msg = "YOUR TURN"
        self.player_turn = True
        self.active_pit = 0
        if self.active_pit_empty():
            self.cycle_cells()

    def active_pit_empty(self):
        player = 1 if self.player_turn else 0
        return self.board_state[player][self.active_pit] == 0

    def update_board_display(self, no_color = False):
        info_msg = "update"
        player = 1 if self.player_turn else 0
        color = 'blue' if self.player_turn else 'red'
        self.board_display[0] = [str(x).rjust(2) if x != 0 else "  " for x in self.board_state[0]]
        self.board_display[1] = [str(x).rjust(2) if x != 0 else "  " for x in self.board_state[1]]
        if no_color:
            return
        self.board_display[player][self.active_pit] = colored(self.board_display[player][self.active_pit], color, attrs=['reverse', 'blink', 'bold'])

    def cycle_cells(self, reverse = False):
        player = 1 if self.player_turn else 0
        for i in range(7):
            adder = 1
            if reverse:
                adder = -1
            self.active_pit = (self.active_pit + adder) % 6
            if not self.active_pit_empty():
                break
            if i >= 6:
                self.game_over = True
                self.info_msg = "GAME OVER"
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
            if key == "q":
                break

            if key == keys.RIGHT:
                self.cycle_cells()

            if key == keys.LEFT:
                self.cycle_cells(reverse = True)

            if key == keys.ENTER:
                self.make_move()
                self.cycle_cells()
                if not self.extra_turn:
                    self.computer_move()
                self.extra_turn = False

            self.update_board_display()

        if not self.game_over:
            clear()
            return

        self.info_msg = "GAME OVER"
        self.update_board_display(no_color=True)
        self.draw_frame()
        while getkey() != 'q':
            continue
        clear()

game = Game()
