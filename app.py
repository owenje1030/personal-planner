import pymongo,json
from flask import Flask,render_template,request, session,redirect
from datetime import datetime, timedelta
import os
import binascii
from flask_wtf.csrf import CSRFProtect
from src.todo import TodoList,Task



app = Flask(__name__)
csrf = CSRFProtect(app)
# Generates a random 24 bit string 
secret_key_value = os.urandom(24)
# Create the hex-encoded string value.
secret_key_value_hex_encoded = binascii.hexlify(secret_key_value)
# Set the SECRET_KEY value in Flask application configuration settings.
app.config['SECRET_KEY'] = secret_key_value_hex_encoded
app.permanent_session_lifetime = timedelta(minutes=15)
client = pymongo.MongoClient("mongodb+srv://owen:owen@cluster0.examw.mongodb.net/?retryWrites=true&w=majority")
db = client['webproj']



@app.route("/")
def index():

    if(session):
        if(session['logged_in']==True):
            return redirect("/home")
        else:
            return redirect("/login")
    else:
        session['logged_in'] = False
        return index()


@app.route("/login", methods=["POST", "GET"])
def login():
    if(request.method=="POST"):
        name = request.form['username']
        password = request.form['password']
        try:
            #Find MongoDB collection for user
            user = db['login'].find_one({'username':name})
            print(user["password"])
            if(str(user["password"]) == password):
                session['logged_in'] = True
                return redirect("/home")
            else:
            
                print(user["password"])
                return redirect("/login") 
            
        except:
            return render_template("/error_msg/user_not_found.html")

    else:
        return render_template("login.html")


@app.route("/register",methods=["POST","GET"])
def register():
    if(request.method=="POST"):
        id = os.urandom(24)
        user = {
            "username" : request.form['username'],
            "password" : request.form['password'],
            "todoID": id
        }
        try:
            exist = db['login'].find_one({user["username"]})
            render_template("/error_msg/register_fail.html")
            return redirect("/register")
        except:
            db['login'].insert_one(user)
            db['schedule'].insert_one({
                "todoID":id,
            })
            session['todoID'] = id
            render_template("/success_msg/register_success.html")
            return redirect("/home")
    
    else:
        return render_template("register.html")
    


@app.route("/home", methods=["GET"])
def home():
    if(session['logged_in'] == True):
        return render_template("home.html")
    else:
        return redirect("/login")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/home")


@app.route("/reminder",methods=["POST","GET"])
def reminder():
    if(session['logged_in']==True):
        #Collect todoID
        id = session['todoID']
        if(request.method=="GET"):

            try:
                    
                todolist = db['schedule'].find_one({'todoID':id})
                tdy = datetime.date()
                return render_template("reminder.html",tdy = tdy, list = todolist)
            
            except:
                print("No TODOLIST record found!")
                return render_template("reminder.html")

        elif(request.method == "POST"):
                #title, desc, deadline, status, importance
                todolist = {
                    "todoID": id,
                    "todoList":{
                        "title":request.form['title'],
                        "desc":request.form['desc'],
                        "deadline":request.form["deadline"],
                        "status":request.form["status"],
                        "importance":request.form["importance"]
                    }
                }
                db['schedule'].update_one(
                    {"todoID":id},
                    {"$set":{"todoList":{
                            "title":request.form['title'],
                            "desc":request.form['desc'],
                            "deadline":request.form["deadline"],
                            "status":request.form["status"],
                            "importance":request.form["importance"]
                        }
                    }})
            

        """ task1 = Task("Task 1","desc","desc","desc","desc")
        list = TodoList()
        list.addTask(task1)
        todolist = list.getList() """

    
    else:
        return redirect('/')



if __name__ == '__main__':
   app.run('0.0.0.0','8080')