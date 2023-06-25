import tictactoe as ttt
import pytest

X = ttt.X
O = ttt.O
E = None


def test_player():
    board = [[E, E, E],
             [E, X, E],
             [E, E, E]]
    assert ttt.player(board) == O

    board = [[E, E, E],
             [E, X, O],
             [E, E, E]]
    assert ttt.player(board) == X


def test_actions():
    board = [[O, X, O],
             [O, X, E],
             [X, O, X]]
    assert ttt.actions(board) == {(1, 2)}

    board = [[E, E, E],
             [E, X, E],
             [E, E, E]]
    assert ttt.actions(board) == {(0, 0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)}


def test_result():
    board = [[E, E, E],
             [E, E, E],
             [E, E, E]]
    assert ttt.result(board, (1, 1)) == [[E, E, E],
                                         [E, X, E],
                                         [E, E, E]]
    
    with pytest.raises(Exception):
        board = [[E, E, E],
                 [E, X, E],
                 [E, E, E]]
        ttt.result(board, (1, 1))


def test_winner():
    board = [[O, X, E],
             [O, X, E],
             [E, X, E]]
    assert ttt.winner(board) == X
    board = [[O, E, X],
             [O, E, X],
             [E, E, X]]
    assert ttt.winner(board) == X
    board = [[X, O, E],
             [X, O, E],
             [X, E, E]]
    assert ttt.winner(board) == X

    board = [[O, O, O],
             [E, X, X],
             [E, X, E]]
    assert ttt.winner(board) == O
    board = [[E, E, X],
             [O, O, O],
             [E, X, X]]
    assert ttt.winner(board) == O
    board = [[E, X, X],
             [E, E, X],
             [O, O, O]]
    assert ttt.winner(board) == O

    board = [[X, O, O],
             [E, X, E],
             [E, E, X]]
    assert ttt.winner(board) == X
    board = [[X, X, O],
             [E, O, E],
             [O, E, X]]
    assert ttt.winner(board) == O


def test_terminal():
    board = [[E, E, E],
             [E, E, E],
             [E, E, E]]
    assert ttt.terminal(board) == False
    board = [[O, X, O],
             [O, X, X],
             [E, O, X]]
    assert ttt.terminal(board) == False
    board = [[X, X, O],
             [E, O, E],
             [O, E, X]]
    assert ttt.terminal(board) == True
    board = [[O, X, O],
             [O, X, X],
             [X, O, X]]
    assert ttt.terminal(board) == True


def test_utility():
    board = [[X, X, O],
             [E, O, E],
             [O, E, X]]
    assert ttt.utility(board) == -1
    board = [[O, X, E],
             [O, X, E],
             [E, X, E]]
    assert ttt.utility(board) == 1
    board = [[O, X, O],
             [O, X, X],
             [E, O, X]]
    assert ttt.utility(board) == 0