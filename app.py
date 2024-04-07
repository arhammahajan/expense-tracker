# Expense Tracker 
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId
import json 
from bson import json_util

client = MongoClient("localhost", 27017)
app = Flask(__name__)

DB = client['expense-tracker']
USERS = DB.users
EXPENSES = DB.expenses

@app.route('/', methods=['GET'])
def index():
    return "<p>This is an expense tracker application</p>"

@app.route('/signup', methods=['POST'])
def signup():
    error = None
    user = dict(username = request.headers["username"], password = request.headers["password"])
    if USERS.find_one(user):
        return "User already exists, please login"         
    USERS.insert_one(user)
    return "User created successfully"

@app.route('/add', methods=['POST'])
def add():
    headers = request.headers
    user = USERS.find_one(dict(username = headers["username"], password = headers["password"]))
    if not user:
        return "User does not exist, please signup"
    expense = EXPENSES.insert_one(dict(userid=user["_id"], amount=headers["amount"],category= headers["category"],description= headers["description"], date=headers["date"]))
    return str(expense.inserted_id)

@app.route('/list', methods=['GET'])
def listexpenses(): 
    headers = request.headers
    user = USERS.find_one(dict(username = headers["username"], password = headers["password"]))
    if not user:
        return "User does not exist, please signup"
    expenses = list(EXPENSES.find({"userid":user["_id"]}))
    return json.loads(json_util.dumps(expenses))

@app.route('/delete', methods=['DELETE'])
def delete():
    headers = request.headers
    user = USERS.find_one(dict(username = headers["username"], password = headers["password"]))
    if not user:
        return "User does not exist, please signup"
    expense = EXPENSES.find_one_and_delete({"_id":ObjectId(headers["id"])})
    if expense:
        return "Expense deleted successfully!"
    
@app.route('/update', methods=['PUT'])
def update():
    headers = request.headers
    user = USERS.find_one(dict(username = headers["username"], password = headers["password"]))
    if not user:
        return "User does not exist, please signup"
    updatedexpense = dict()
    updatedexpense["$set"] = dict(userid=user["_id"], amount=headers["amount"],category= headers["category"],description= headers["description"], date=headers["date"])
    expense = EXPENSES.find_one_and_update({"_id":ObjectId(headers["id"])}, updatedexpense)
    print(expense)
    if expense:
        return "Expense updated successfully!"