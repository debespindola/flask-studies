from flask import Flask, request, render_template, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'alura'

class Game:
    def __init__(self, name, category, console):
        self.name = name
        self.category = category
        self.console = console

class User:
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

user1 = User('debs', 'Deborah', '1234')
user2 = User('kev', 'Kevin', '1234')

users = {user1.id: user1, user2.id: user2}

game1 = Game('Super Mario', 'Action', 'SNES')
game2 = Game('Mortal Kombat', 'Fight', 'SNES')
list_of_games = [game1, game2]

@app.route('/')
def RenderHome():
    return render_template(
        'list.html', 
        title='Games',
        games=list_of_games
    )

@app.route('/form')
def RenderForm():
    if 'user_logged' not in session or session['user_logged'] == None:
        return redirect(url_for('Login', next=url_for('RenderForm')))

    return render_template(
        'newGame.html',
        title='Add new game'
    )

@app.route('/create', methods=['POST',])
def CreateGame():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']

    newGame = Game(name, category, console)

    list_of_games.append(newGame)
    return redirect(url_for('RenderHome'))

@app.route('/login')
def Login():
    next = request.args.get('next')
    return render_template('login.html', title="Login", next=next)

@app.route('/auth', methods=['POST',])
def Authenticate():
    if request.form['user'] in users:
        user = users[request.form['user']]

        if user.password == request.form['passcode']:
            session['user_logged'] = user.id

            flash(user.name + ' successfully logged')

            next_page = request.form['next']

            return redirect(next_page)
        
        else: 
            flash('Unauthorized, ty again.')
        return redirect(url_for('Login'))
    else:
        flash('Unauthorized, ty again.')
        return redirect(url_for('Login'))

@app.route('/logout')
def Logout():
    session['user_logged'] = None
    flash('No user logged')
    return redirect(url_for('RenderHome'))

app.run(debug=True)
