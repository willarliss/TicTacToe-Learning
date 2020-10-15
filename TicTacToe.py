import os
import sys
import numpy as np
import pandas as pd



class Board:
    
    def __init__(self):
        
        self.board = np.zeros(9).reshape(3,3)
        
    def reset(self):
        
        self.board = np.zeros(9).reshape(3,3)
        return self
    
    def player_1(self, pos):
        
        try:
            if self.board.reshape(1,-1)[0][int(pos)-1] != 0:
                return 'bad'
            else:
                np.put(self.board, int(pos)-1, 1)
        except:
            return 'bad'

    def player_2(self, pos):
        
        try:
            if self.board.reshape(1,-1)[0][int(pos)-1] != 0:
                return 'bad'
            else:
                np.put(self.board, int(pos)-1, 2)
                return 'good'
        except:
            return 'bad'
    
    def evaluate(self):
        
        solutions = [
            self.board[:,0], 
            self.board[:,1],
            self.board[:,2],
            self.board[0,:],
            self.board[1,:],
            self.board[2,:],
            np.diag(self.board),
            np.diag(self.board[::,::-1]),
            ]
            
        for solution in solutions:
            
            if set(solution) == {1} or set(solution) == {2}:
                self.winner = f'Player {int(solution[0])}'
                return 'end'
            
        if 0 not in self.board.reshape(1,-1)[0]:
            self.winner = 'tie'
            return 'end'
            
        return 'cont'
    
    def display(self):
        
        X = []
        for x in self.board.reshape(1,-1)[0]:
            
            if x == 1:
                X.append('X')
            if x == 2:
                X.append('O')
            if x == 0:
                X.append(' ')

        print('     |     |     ')
        print(f'  {X[0]}  |  {X[1]}  |  {X[2]}  ')
        print('_____|_____|_____')
        print('     |     |     ')
        print(f'  {X[3]}  |  {X[4]}  |  {X[5]}  ')
        print('_____|_____|_____')
        print('     |     |     ')
        print(f'  {X[6]}  |  {X[7]}  |  {X[8]}  ')
        print('     |     |     ')
     


class Computer:
    
    def __init__(self):
        
        self.memory = {}
        
    def move(self, board):
        
        try:
            move = np.random.choice(self.memory[board])
        except:
            move = np.random.randint(1, 10)
        return move
    
    def commit(self, moves):
        
        for move in moves:
            
           if move in self.memory:
               self.memory[move].append(moves[move])
           else:
               self.memory[move] = [moves[move]]
               
    def remove(self, moves):
        
        for move in moves:
            if move in self.memory:

                try:
                    self.memory[move].remove(moves[move])
                except ValueError:
                    pass

    def store_dta(self, name):
        
        names = ['state', 'move']    
        data = [ [i[0],i[1]] for i in self.memory.items() ]
       
        self.df = pd.DataFrame(data, columns=names)  
        self.df.to_csv(name, index=False, header=True)
    
    def load_dta(self, name):
        
        df = pd.read_csv(name)
        self.df = df.copy(deep=True)
        
        mem = {s:m for s,m in zip(df['state'], df['move'])}
        self.memory = {eval(k):list(eval(v)) for k,v in mem.items()}
        
        return mem
        
    def transition_matrix(self, as_board=True):
        
        transition_m = {}
        transitions = {}

        for i in self.memory:

            moves = np.array(self.memory[i]).astype(int)
            if len(moves) == 0:
                continue

            transition_m[i] = {e:list(moves).count(e)/len(moves) for e in np.arange(10)}
            transitions[i] = np.array([list(moves).count(e)/len(moves) for e in np.arange(1,10)]).reshape(3,3)
            
        if as_board:
            return transitions
        else:
            return transition_m
    
        
        
        

class TicTacToe:
    
    def __init__(self):
        
        self.comp = Computer()
        self.board = Board()
        
    def CvC(self, iterations=1000, rand=True):
        
        win, n = [], []
        
        for r in range(iterations):
            
            print('Game', r+1)
            
            state = 'cont'  
            self.board.reset()
            p1_moves, p2_moves = {}, {}
            turn = np.random.randint(1,3)
            
            ###
            
            while state == 'cont':
                b = tuple(np.copy(self.board.board.reshape(1,-1)[0]))
                
                if turn%2 == 0:
                    attempt = 'bad'
                    while attempt == 'bad':
                        
                        move = np.random.randint(1,10)
                        
                        attempt = self.board.player_1(move)
                        p1_moves[b] = move
                            
                if turn%2 != 0:
                    attempt = 'bad'
                    while attempt == 'bad':
                        
                        if rand:
                            move = np.random.randint(1,10)
                        else:
                            move = self.comp.move(b)
                            
                        attempt = self.board.player_2(move)
                        p2_moves[b] = move
                    
                state = self.board.evaluate()
                turn += 1
                    
            ###
            
            print('Winner:', self.board.winner) 
            
            p1_moves_new = {}
            for move in p1_moves:
                move = np.array(move)
                
                x = np.where(move==1, 3, move)
                y = np.where(x==2, 1, x)
                z = np.where(y==3, 2, y)
                p1_moves_new[tuple(z)] = p1_moves[tuple(move)]
                    
            if self.board.winner == 'Player 1':            
                self.comp.commit(p1_moves_new)
                if rand == False:
                    self.comp.remove(p2_moves)
                win.append(0)
                    
            if self.board.winner == 'Player 2':
                self.comp.commit(p2_moves)
                if rand == False:
                    self.comp.remove(p1_moves_new)
                win.append(1)
                
            n.append(r+1)
            print()
    
        return pd.DataFrame(list(zip(n,win)), columns=['game', 'win'])
    
    def PvC(self, rand=False):
        
        again = 'y'
        
        while again == 'y':
            
            state = 'cont'  
            self.board.reset()
            p1_moves, p2_moves = {}, {}
            turn = np.random.randint(1,3)            
            
            ###
            
            while state == 'cont':
                self.board.display()
                b = tuple(np.copy(self.board.board.reshape(1,-1)[0]))
                
                if turn%2 == 0:
                    attempt = 'bad'
                    while attempt == 'bad':
                        
                        move = input('Player 1 (X): ')                        
                        
                        attempt = self.board.player_1(move)
                        p1_moves[b] = move
                            
                if turn%2 != 0:
                    attempt = 'bad'
                    while attempt == 'bad':
                        
                        if rand:
                            move = np.random.randing(1,10)
                        else:
                            move = self.comp.move(b)
                            
                        attempt = self.board.player_2(move)
                        p2_moves[b] = move
                        
                    print(f'\nPlayer 2 (O): {move}')
                    
                state = self.board.evaluate()
                turn += 1
                
            ###
            
            self.board.display()
            print('\nWinner:', self.board.winner) 
            
            p1_moves_new = {}
            for move in p1_moves:    
                move = np.array(move)
            
                x = np.where(move==1, 3, move)
                y = np.where(x==2, 1, x)
                z = np.where(y==3, 2, y)
                p1_moves_new[tuple(z)] = p1_moves[tuple(move)]
            
            if self.board.winner == 'Player 1':
                self.comp.commit(p1_moves_new)
                self.comp.remove(p2_moves)
                        
            if self.board.winner == 'Player 2':
                self.comp.commit(p2_moves)
                self.comp.remove(p1_moves_new)
            
            again = input("Press 'Y' to play again   ").lower()
            print()    
            
    def PvP(self):
        
        again = 'y'
        
        while again == 'y':
            
            state = 'cont'  
            self.board.reset()
            p1_moves, p2_moves = {}, {}
            turn = np.random.randint(1,3)
                    
            ###
            
            while state == 'cont':
                self.board.display()
                b = tuple(np.copy(self.board.board.reshape(1,-1)[0]))
                
                if turn%2 == 0:
                    attempt = 'bad'
                    while attempt == 'bad':
                        
                        move = input('Player 1 (X): ')                        
                        
                        attempt = self.board.player_1(move)
                        p1_moves[b] = move
                            
                if turn%2 != 0:
                    attempt = 'bad'
                    while attempt == 'bad':
                        
                        move = input('Player 2 (O): ')                        

                        attempt = self.board.player_2(move)
                        p2_moves[b] = move
                                            
                state = self.board.evaluate()
                turn += 1
                
            ###
            
            self.board.display()
            print('\nWinner:', self.board.winner) 
            
            again = input("Press 'Y' to play again   ").lower()
            print()


###


def test():
    
    ttt = TicTacToe()
    ttt.CvC()
        


