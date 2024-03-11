from flask import Flask, render_template, make_response, url_for, request, session
import json
from database import check_auth
import database
#from constructer_effect import ConstructProgect
import os
from random import randint

#Создание приложения и уникальной подписи
app = Flask(__name__)
app.config['SECRET_KEY']='734bc427f6301f5effe583435dc1145e4cedb695s'


users_projects={}

#Страница авторизации
@app.route('/')
def login_page():
    if 'user' in session:
        if session['user']=='success':
            return render_template('home.html')
        elif session['user']=='fail': return 'False'
            #return render_template('nologincorrect.html')
    else:
        return render_template('index.html')

#Обработка попытки войти
@app.route('/login', methods=['POST'])
def login():
    if request.method=='POST':
        #Приём данных
        data=json.loads(request.data.decode(encoding='utf-8'))
        login=data['login']
        password=data['password']

        #Обработка данных
        if check_auth(login=login, password=password):
            session['user']='success'
            session['user_id']=str(randint(99999,999999))
            database.add(session['user_id'])
            return render_template('home.html')
        else:
            #session['user']='fail'
            return 'False'

#Обработка попытки выйти
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return render_template('index.html')

#Получение данных из куки
@app.route('/getcoockie', methods=['GET'])
def getcoockie():
    return database.get(session['user_id'])

#Запись данных в куки
@app.route('/setcoockie', methods=['POST'])
def setcoockie():
    data=json.loads(request.data.decode(encoding='utf-8'))
    usercell=database.get(session['user_id'])
    
    for params in data:
        if params=='delete':
            del usercell[data['delete']][str(data['id'])]
            
            try:
                constructor=users_projects[str(session['user_id'])]
                constructor.DeleteEffect(int(data['id']))
                constructor.GetFullLayout(session['user_id'])
            except Exception as error:
                print(error)
            
        else:
            usercell[params]=data[params]
    database.save(session['user_id'],usercell)
    print(database.get(session['user_id']))
    return dict(usercell)

#Получение айди фотоподложки
@app.route('/getlayout', methods=['POST'])
def getlayout():
    data=json.loads(request.data.decode(encoding='utf-8'))
    usercell=database.get(session['user_id'])
    if session['user_id']:
        users_projects[str(session['user_id'])]=ConstructProgect(
            int(data['project_width']),
            int(data['project_height']),
            str(session['user_id'])
        )
        usercell['element']=users_projects[str(session['user_id'])].lays
        database.save(session['user_id'],usercell)
    return str(session['user_id'])

@app.route('/addshrift', methods=['POST'])
def addshrift():
    print('letsgo')
    data=json.loads(request.data.decode(encoding='utf-8'))
    usercell=database.get(session['user_id'])
    constructor=users_projects[str(session['user_id'])]
    constructor.AppendObjectText()
    constructor.GetFullLayout(session['user_id'])
    usercell['element']=users_projects[str(session['user_id'])].lays
    database.save(session['user_id'],usercell)
    return str(session['user_id'])

app.run()
