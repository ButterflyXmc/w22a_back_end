# four import from flask for flask responses eg
from flask import Flask, request, make_response, jsonify
from dbhelpers import run_statement
import json

app = Flask(__name__)

@app.get('/api/candy')
def get_candy():
    result = run_statement("CALL get_candy()")
    if(type(result) == list):
        return json.dumps(result, default=str)
    else:
        return "Something went wrong"

@app.post('/api/candy')
def post_candy():
    name_input = request.json.get('candyName')
    description_input = request.json.get('candyDescription')
    if name_input == None:
        return "You must enter a name!"
    result = run_statement("CALL post_candy(?,?)", [name_input, description_input])
    if description_input == None:
        return "Your must enter a description!"
    else:
        return "Something went wrong!"

@app.patch('/api/candy')
def update_candy():
    id_input = request.json.get('candyId')
    description_input = request.json.get('candyDescription')
    if id_input == None:
        return "You must enter a valid candy ID!"
    result = run_statement("CALL update_candy(?,?)", [id_input, description_input])
    if description_input == None:
        return "Your must enter a description!"
    else:
        return "Something went wrong!"

@app.delete('/api/candy')
def delete_candy():
    id_input = request.json.get('candyId')
    if id_input == None:
        return "You must enter a valid candy ID!"
    result = run_statement("CALL delete_candy(?)", [id_input])
    if result == None:
        return "Animal deleted Successfully"
    else:
        return "Something went wrong!"

        



app.run(debug = True)