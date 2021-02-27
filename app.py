from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os

app = Flask(__name__)


app.config['MONGO_URI']=os.environ.get('TODO_LIST_APP_MONGO')
mongo = PyMongo(app)


@app.route('/', methods=["GET","POST"])
def index():
    todos_collection = mongo.db.todos
    todos=todos_collection.find()
    return render_template('index.html',todos = todos)

@app.route('/add_todo', methods =["POST"])
def add_todo():
    todos_collection = mongo.db.todos
    todo_item = request.form.get('add-todo')
    todos_collection.insert_one({'text':todo_item, 'complete':False})

    return redirect(url_for('index'))

@app.route("/complete_todo/<oid>")
def complete_todo(oid):
    todos_collection = mongo.db.todos
    todo_item = todos_collection.find_one({'_id':ObjectId(oid)})
    todo_item['complete'] = True
    todos_collection.save(todo_item)
    return redirect(url_for('index'))

@app.route("/delete_completed")
def delete_completed():
    todos_collection  = mongo.db.todos
    todos_collection.delete_many({'complete':True})
    return redirect(url_for('index'))

@app.route("/delete_all")
def delete_all():
    todos_collection  = mongo.db.todos
    todos_collection.delete_many({})
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug = True)
