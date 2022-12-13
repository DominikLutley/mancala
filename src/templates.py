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

