from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = 'Great Number'

@app.route('/', methods=['GET', 'POST'])
def root_route():
    if request.method == 'GET':
        if 'the_number' not in session:
            session['the_number'] = random.randint(1, 100)
            session['end_game'] = False
            session['color'] = 'red'
            session['count'] = 0
        print(session['the_number'])

    if request.method=='POST':
        if session['count'] < 6:
            session['guess'] = int(request.form['guess'])
            if session['guess'] < session['the_number'] and (not session['end_game']):
                session['hint'] = "Too Low!"
                session['count'] += 1
            elif session['guess'] > session['the_number'] and (not session['end_game']):
                session['hint'] = "Too High!"
                session['count'] += 1
            else:
                session['hint'] = str(session['the_number'])+" was the number!"
                session['end_game'] = True
                session['color'] = 'green'
            return redirect('/')
        else:
            session['hint'] = "You Lose"
            session['end_game'] = True
            return redirect('/')

    return render_template("index.html")

@app.route('/play_again', methods=['POST'])
def play_again():
    if 'the_number' in session:     # check leaderboard before game start; cause error when click play again (session variables do not exist)
        session.pop('the_number')
    if 'guess' in session:
        session.pop('guess')
    if 'hint' in session:
        session.pop('hint')
    if 'color' in session:
        session.pop('color')
    if 'count' in session:
        session.pop('count')
    if 'end_game' in session:
        session.pop('end_game')
    # session.clear()
    return redirect('/')

@app.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    if request.method == 'POST':
        if 'leaderboard' not in session:
            session['leaderboard'] = []
        winner_list = session['leaderboard']
        winner = {'player_name': request.form['player'], 'number_attempt': session['count']}
        winner_list.append(winner)
        session['leaderboard'] = winner_list
        return redirect('/leaderboard')

    if request.method == 'GET':
        return render_template("leaderboard.html") 


if __name__=="__main__":
    app.run(debug=True)