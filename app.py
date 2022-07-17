import imp
from importlib.resources import contents
from unicodedata import name
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import Sentiment_Analysis
import math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
sent_list = []
GPE_exist = False
PERSON_exist = False
EVENT_exist = False
ORG_exist = False
LOC_exist = False

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), default='ANONYMOUS')
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return  '<Task %r>' % self.id

#https://stackoverflow.com/questions/14525029/display-a-loading-message-while-a-time-consuming-function-is-executed-in-flask
@app.route('/', methods=['POST','GET'])
def index():
    global GPE_exist
    global PERSON_exist
    global EVENT_exist
    global ORG_exist
    global LOC_exist
    global sent_list
    if request.method == 'POST':
        Sentiment_par = ""
        """
        if request.form.get("content"):
            task_content = request.form['content']
            new_task = Todo(content=task_content)
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return "Error occured adding your task"

        #this is for manual inputs
        """
        """
        elif request.form.get("hint_content"):
            return render_template('index.html', Sentiment=, Hint=Sentiment_Analysis.get_hint(sent_list[1]))
        """
        if request.form.get("get_content"):
            sent_list.clear()
            return redirect('/')
        elif request.form.get("board_content"):
            sent_list.clear()
            return redirect('/leaderboard')
        elif request.form.get("country_content"):
            try:
                Country = request.form['country_content']
                #return render_template('index.html', Display_Error=True, Error_Type="That Year that is not an integer. Please input an integer.")
                #if the country contene exist, we input Country
                r_list = Sentiment_Analysis.random_cntry_yr(Country)
                year_content = r_list[0]
                Country = r_list[1]
                Sentiment_par=Sentiment_Analysis.year_api(year_content, Country)
                if not Sentiment_par:
                    return render_template('index.html', Display_Error=True, Error_Type="The Country you inputted was incorrect or the random year was not found in the backend. Please try again")
                #if there is any response then we can append, else we return
                map_par = Sentiment_Analysis.NER(Sentiment_par)
                Sentiment_par = map_par[1]
                if Sentiment_par:
                    sent_list.append(Sentiment_par)
                    sent_list.append(map_par[0])
                    GPE_exist = Sentiment_Analysis.Look_for_key(sent_list[1],"GPE")
                    PERSON_exist = Sentiment_Analysis.Look_for_key(sent_list[1],"PERSON")
                    EVENT_exist = Sentiment_Analysis.Look_for_key(sent_list[1],"EVENT")
                    ORG_exist = Sentiment_Analysis.Look_for_key(sent_list[1],"ORG")
                    LOC_exist = Sentiment_Analysis.Look_for_key(sent_list[1],"LOC")
                else:
                    return render_template('index.html', Display_Error=True, Error_Type="Looks like Data did not exist for that random year. Please try again")
                return render_template('index.html', Sentiment=Sentiment_Analysis.split_paragraph(Sentiment_par), Current_Year=year_content, Current_Country=Country, GPE = GPE_exist, PERSON=PERSON_exist, EVENT=EVENT_exist, ORG=ORG_exist, LOC=LOC_exist, Hint=Sentiment_Analysis.get_hint(sent_list[1]))
            except:
                return render_template('index.html', Display_Error=True, Error_Type="Unexpected error Occured try again.")
        elif request.form.get("random_content"):
            l = Sentiment_Analysis.random_cntry_yr()
            Sentiment_par=Sentiment_Analysis.year_api(l[0], l[1])
            map_par = Sentiment_Analysis.NER(Sentiment_par)
            Sentiment_par = map_par[1]
            if Sentiment_par:
                sent_list.append(Sentiment_par)
                sent_list.append(map_par[0])
                GPE_exist = Sentiment_Analysis.Look_for_key(sent_list[1],"GPE")
                PERSON_exist = Sentiment_Analysis.Look_for_key(sent_list[1],"PERSON")
                EVENT_exist = Sentiment_Analysis.Look_for_key(sent_list[1],"EVENT")
                ORG_exist = Sentiment_Analysis.Look_for_key(sent_list[1],"ORG")
                LOC_exist = Sentiment_Analysis.Look_for_key(sent_list[1],"LOC")
            else:
                return render_template('index.html', Display_Error=True, Error_Type="Looks like the backend did not find information on a random year. Please try again.")
            return render_template('index.html', Sentiment=Sentiment_Analysis.split_paragraph(Sentiment_par), Current_Year=l[0], Current_Country=l[1], GPE = GPE_exist, PERSON=PERSON_exist, EVENT=EVENT_exist, ORG=ORG_exist, LOC=LOC_exist, Hint=Sentiment_Analysis.get_hint(sent_list[1]))
        elif request.form.get("Sent_Guess") and sent_list:
            Out = ""
            #try to catch integer exception
            try:    
                Guess = int(request.form['Sent_Guess'])
            except:
                return render_template('index.html', Display_Error=True, Error_Type="The Sentiment Guess was not an integer")
            #sent_list[1] is the answer
            Score = Sentiment_Analysis.sentiment_scores(sent_list[0])
            Score = math.trunc(Score['compound']*100)
            Player_score = Sentiment_Analysis.Get_points(Guess,Score)
            if GPE_exist:
                GPE = request.form['GPE_content']
                if Sentiment_Analysis.guess_blank(sent_list[1],"GPE",GPE):
                    Out += "GPE guess was correct. +10  "
                    Player_score += 10
            if PERSON_exist:
                PERSON = request.form['PERSON_content']
                if Sentiment_Analysis.guess_blank(sent_list[1],"PERSON", PERSON):
                    Out += "PERSON guess was correct. +10 "
                    Player_score += 10
            if EVENT_exist:
                EVENT = request.form['EVENT_content']
                if Sentiment_Analysis.guess_blank(sent_list[1],"EVENT", EVENT):
                    Out += "EVENT guess was correct. +10 "
                    Player_score += 10
            if ORG_exist:
                ORG = request.form['ORG_content']
                if Sentiment_Analysis.guess_blank(sent_list[1],"ORG", ORG):
                    Out += "ORG guess was correct. +10 "
                    Player_score += 10
            if LOC_exist:
                LOC = request.form['LOC_content']
                if Sentiment_Analysis.guess_blank(sent_list[1],"LOC", LOC):
                    Out += "ORG guess was correct. +10 "
                    Player_score += 10

            #this is a dic
            if request.form.get("name_content"):
                Name_Content = request.form['name_content']
                task = Todo(content=Player_score, name=Name_Content)
            else:
                task = Todo(content=Player_score)
            #sent_list.clear()
            try:
                db.session.add(task)
                db.session.commit()
                return render_template('index.html', Guess_Sentiment=Player_score, Comp_Score=Score, Player_Guess=Guess, Display_Guess=True, Blank_Guess=Out, Answer=sent_list[1])
            except:
                return render_template('index.html', Display_Error=True, Error_Type="There as an Error processing the Database")
        else:
            return redirect('/')
    else:
        return render_template('index.html')
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/leaderboard')
    except:
        return 'There was a problem deleting that task'

@app.route('/delete_last')
def delete_last():
    tasks = Todo.query.order_by(Todo.content.desc()).all()
    for task in tasks:
        today = datetime.today()
        datem = datetime(today.year, today.month, today.day)
        if task.date_created.date() < datem.date():
            try:
                task_to_delete = Todo.query.get_or_404(task.id)
                db.session.delete(task_to_delete)
                db.session.commit()
            except:
                return 'There was a problem deleting that task'
        else:
            return render_template('leaderboard.html', Nothing=True)
    return redirect('/leaderboard')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/leaderboard')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)

@app.route('/leaderboard', methods=['POST','GET'])
def leaderboard():
    tasks = Todo.query.order_by(Todo.content.desc()).all()
    return render_template('leaderboard.html', tasks=tasks)

if __name__ == "__main__":
    db.session.flush()
    app.run(debug=True)