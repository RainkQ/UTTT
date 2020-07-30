#!/usr/bin/env python3

import sys
from players import Random, MSTCPlayer
from engine import MainBoard, Player


def simulate(player1, player2):
    s = Player.ONE
    while not player1.main_board.is_finished:
        print(s)
        if s == Player.ONE:
            main_coor, sub_coor = player1.get_my_move()
            player1.add_my_move(main_coor, sub_coor)
            player2.add_opponent_move(main_coor, sub_coor)
            s = Player.TWO
        else:
            main_coor, sub_coor = player2.get_my_move()
            player1.add_opponent_move(main_coor, sub_coor)
            player2.add_my_move(main_coor, sub_coor)
            s = Player.ONE
        print("\t{}, {}".format(main_coor, sub_coor))
        sys.stdout.flush()
    return player1.main_board.winner

if __name__ == "__main__":
    num_round = 50
    p1, p2, tie = 0, 0, 0
    for i in range(num_round):
        player1 = MSTCPlayer(True)
        player2 = MSTCPlayer(False)
        # player2 = Random()

        # simualte game and record the result
        res = simulate(player1, player2)
        if res == Player.ME:
            p1 += 1
        elif res == Player.OPPONENT:
            p2 += 1
        else:
            tie += 1
    print("p1:{}, p2:{}, tie:{}".format(p1, p2, tie))
