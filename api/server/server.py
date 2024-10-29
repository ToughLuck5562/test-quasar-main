from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import .account_database
import .activites_database

app = Flask(__name__, template_folder='../client/templates', static_folder='../client/static')
app.secret_key = 'quasarkey'

@app.route('/', methods=['POST', 'GET'])
def main():
    return render_template("main.html")

@app.route('/get-activity', methods=['GET'])
def get_activity():
    tags = request.args.getlist('tags') 
    level = request.args.get('level')

    if level is None or not tags:
        return jsonify({"error": "Level and tags are required"}), 400
    
    fetched = activites_database.GetActivities(level, tags)
    return jsonify(fetched)

@app.route('/get-account-tags', methods=['GET'])
def get_account_tags(): 
    username = request.args.get('username')
    
    if username:
        ValidAccount = account_database.ValidateAccount(username)
        if ValidAccount:
            return jsonify(ValidAccount['account_activities_tags'])
        else:
            return jsonify('Failed')
    else:
        return jsonify('Failed')

@app.route('/pricing', methods=['POST', 'GET'])
def pricing():
    return render_template("pricing.html")

@app.route('/terms-conditions', methods=['POST', 'GET'])
def terms_conditions():
    return render_template("terms_conditions.html")

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if 'username' in session:
        ValidAccount = account_database.ValidateAccount(session['username'])
        
        if ValidAccount != 400:
            return render_template("dashboard.html", username=ValidAccount['username'], account_level=ValidAccount['account_level'], account_activities_tags=ValidAccount['account_activities_tags'])
        else:
            session.pop('username', None)
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
    
@app.route('/ai-playground', methods=['POST', 'GET'])
def ai_playground():
    if 'username' in session:
        return render_template("aiplayground.html", username=session['username'])
    else:
        return redirect(url_for('main'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "GET":
        if 'username' in session:
            return redirect(url_for('dashboard'))
        return render_template("login.html")
    elif request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        username, response = account_database.LoginToAccount(email, password)
        if response == 200:
            session['username'] = username
            return redirect(url_for('dashboard'))
            
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "GET":
        if 'username' in session:
            return redirect(url_for('dashboard'))
        else:
            return render_template('signup.html')
    elif request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        username, response = account_database.CreateAccount(account_database.AccountClass(username, password, email, 0, ['math', 'simple', 'addition'], 0, 'None'))
        if response == 200:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return jsonify('Fail')

if __name__ == "__main__":
    
    app.run(debug=True)
