from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)
xState = [0] * 9
zState = [0] * 9
turn = 1  # 1 = player, 0 = computer

def checkWin(xState, zState):
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for win in wins:
        if sum([xState[i] for i in win]) == 3:
            return "X"
        if sum([zState[i] for i in win]) == 3:
            return "O"
    return None

def computerMove():
    available_positions = [i for i in range(9) if xState[i] == 0 and zState[i] == 0]
    return random.choice(available_positions) if available_positions else -1

@app.route('/')
def index():
    winner = checkWin(xState, zState)
    return render_template('index.html', xState=xState, zState=zState, winner=winner)

@app.route('/move/<int:pos>')
def move(pos):
    global turn
    if xState[pos] == 0 and zState[pos] == 0 and turn == 1:
        xState[pos] = 1
        turn = 0

    if turn == 0:
        comp_pos = computerMove()
        if comp_pos != -1:
            zState[comp_pos] = 1
            turn = 1
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    global xState, zState, turn
    xState = [0] * 9
    zState = [0] * 9
    turn = 1
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
