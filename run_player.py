#!/usr/bin/env python3

import sys
from argparse import ArgumentParser
from players import Random, MSTCPlayer


def main(p):
    line = sys.stdin.readline()
    while line:
        p.process_input(line.strip())
        line = sys.stdin.readline()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-t", "--type", help="type player, 0:random, 1:mstc", default=1, type=int)

    args = parser.parse_args()
    player = Random()
    if args.type == 1:
        player = MSTCPlayer()
    main(player)