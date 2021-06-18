from flask import Flask, render_template, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import timedelta
from claculations import Equation_calc, totex, format
from pytexit import py2tex

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
app.secret_key = "somesecretkey"
db = SQLAlchemy(app)

class Equation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equation = db.Column(db.String(200), nullable=False)
    inputs = db.Column(db.Text, nullable=False)
    latex = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200), nullable=False)
    title_ar = db.Column(db.String(200), nullable=False)
    info_en = db.Column(db.String(2000), nullable=True)
    info_ar = db.Column(db.String(2000), nullable=True)
    img = db.Column(db.String(500), nullable=True)
    video = db.Column(db.String(400), nullable=True)

class CustomModelView(ModelView):
    def is_accessible(self):
        if 'is_admin' in session:
            return True
        return False

admin = Admin(app)
admin.add_view(CustomModelView(Equation, db.session))
# Force the session to be closed otherwise it will close with the closure of the browser
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=50)

@app.route('/')
def index():
    try:
        equations = Equation.query.order_by(Equation.id).all()
        return render_template('index.html', equations=equations)
    except:
        pass
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # if request.form['username'] == '123' and request.form['password'] == 'abc':
        session['is_admin'] = True
        return redirect('/admin')
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'is_admin' in session:
        session.pop('is_admin')
    return redirect(url_for('index'))

@app.route('/calculator/<int:id>', methods=['POST', 'GET'])
def calculator(id):
    eq = Equation.query.get(id)
    eqs = Equation.query.all()
    if request.method == 'POST':
        try:
            eqq = Equation_calc(eq.equation)
            input_map = {}
            solving_for = None
            for inp in request.form:
                if request.form[inp] != "":
                    input_map[inp] = request.form[inp]
                else:
                    solving_for = inp
            result = eqq.solve_equation(input_map)
            if type(result) is dict:
                raise TypeError
            output_map = input_map.copy()
            output_map[solving_for] = result
            tex = totex(solving_for + '=' + format(result))
            return render_template('calculator.html', equation=eq, output=output_map, equations=eqs, tex=tex)
        except Exception as e:
            print(e)
            return render_template('calculator.html', equation=eq, output={}, equations=eqs)
    return render_template('calculator.html', equation=eq, output={}, equations=eqs)

if __name__ == '__main__':
    app.run(debug=True)