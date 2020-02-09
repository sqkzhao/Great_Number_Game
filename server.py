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
    session.clear()
    return redirect('/')

@app.route('/leaderboard', methods=['GET','POST'])
def leaderboard():
    if request.method == 'POST':
        if 'leaderboard' not in session:
            session['leaderboard'] = {}
        session['leaderboard']['player_name'] = request.form['player']
        session['leaderboard']['number_attempt'] = session['count']
        return redirect('/leaderboard')

    if request.method == 'GET':
        if 'leaderboard' not in session:
            session['leaderboard'] = {}
            
    return render_template("leaderboard.html")

if __name__=="__main__":
    app.run(debug=True)