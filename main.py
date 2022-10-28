from getkey import getkey, keys
from termcolor import colored
import os

FORMAT = """
             ╔════════════════════╗
             ║ WELCOME TO MANCALA ║
             ╚════════════════════╝

                       ◀◀◀
    ┏━━━━┯━━━━┯━━━━┯━━━━┯━━━━┯━━━━┯━━━━┯━━━━┓
    ┃    │ {self.board_display[0][5]} │ {self.board_display[0][4]} │ {self.board_display[0][3]} │ {self.board_display[0][2]} │ \
{self.board_display[0][1]} │ {self.board_display[0][0]} │    ┃
    ┃ {self.board_display[0][6]} ├────┼────┼────┼────┼────┼────┤ {self.board_display[1][6]} ┃
    ┃    │ {self.board_display[1][0]} │ {self.board_display[1][1]} │ {self.board_display[1][2]} │ {self.board_display[1][3]} │ \
{self.board_display[1][4]} │ {self.board_display[1][5]} │    ┃
    ┗━━━━┷━━━━┷━━━━┷━━━━┷━━━━┷━━━━┷━━━━┷━━━━┛
                       ▶▶▶


  {self.info_msg}
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
        self.update_board_display()

    def draw(self):
        for _i in range(2):
            clear()
            print(FORMAT.format(**locals()))

    def make_move(self):
        idx = self.active_pit
        stone_num = self.board_state[1][idx]
        self.board_state[1][idx] = 0
        for i in range(stone_num):
            j = i + idx + 1
            j = j % 14
            if j > 6:
                self.board_state[0][j % 7] = self.board_state[0][j % 7] + 1
            else:
                self.board_state[1][j] = self.board_state[1][j] + 1

    def update_board_display(self):
        info_msg = "update"
        self.board_display[0] = [str(x).rjust(2) if x != 0 else "  " for x in self.board_state[0]]
        self.board_display[1] = [str(x).rjust(2) if x != 0 else "  " for x in self.board_state[1]]
        self.board_display[1][self.active_pit] = colored(self.board_display[1][self.active_pit], 'blue', attrs=['reverse', 'blink', 'bold'])

    def cycle_cells(self, reverse = False):
        for i in range(6):
            adder = 1
            if reverse:
                adder = -1
            self.active_pit = (self.active_pit + adder) % 6
            if self.board_state[1][self.active_pit] != 0:
                break
            if i >= 5:
                self.game_over = True
                break

    def loop(self):
        while self.game_over == False:
            self.draw()

            key = getkey()
            if key == "q":
                break

            if key == keys.RIGHT:
                self.cycle_cells()

            if key == keys.LEFT:
                self.cycle_cells(reverse = True)

            if key == keys.ENTER:
                self.make_move()
                self.cycle_cells(reverse = True)

            self.update_board_display()

        clear()

game = Game()
game.loop()
