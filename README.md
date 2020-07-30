# Ultimate TicTacToe - Python Player & Game Engine

## How to Run

* connect server
    ```bash
    ./connect.sh 0 "replace-with-lobby-name" # run random player
    ./connect.sh 1 "replace-with-lobby-name" # run basic mcts player
    ```

* local run
    ```bash
    python local_auto_run.py # two local players compete each other
    ```
## TODO

* [ ] warm start, construct initial tree when creating the player

## Dev Log

* [7.24] Add tree node reuse. 36 win out of 50 matches competing against basic MSTC players.
* [7.23] Add inplace board move to improve performance & Fix bug in MCST
* [7.22] Monte Carlo Search Tree Basic Version

## Meeting Log

* [7.23] all members
    * Read & learn MCST code & game framework
    * Goal: find heuristic evaluation functions