# TicTacToe-Learning
This project builds a Markov Chain model that iteratively improves its TicTacToe performance. The file test.py offers functions for building the chain, evaluating its performance, and playing against it. The model plays against a random number generator and stores the board states and successive move of the winning agent. The model can then call on those board states to determine its next move.

Data for the chain is not included in this repository. In order to build data for the chain, use test.py to execute the 'train' function. Pass the arguments cold=True, name='data.csv', and n=1_000_000. Next execute the 'play' function passing the argument name='data.csv'.
