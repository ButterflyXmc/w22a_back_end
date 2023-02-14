# four import from flask for flask responses eg
from flask import Flask, request, make_response, jsonify
from dbhelpers import run_statement
# adding CROS so it will accept requests from different origins
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


# ! DISPLAYS CANDIES
@app.get('/api/candy')
def get_candy():
    result = run_statement("CALL get_candy()")
    keys = ["Id", "Name", "Description"]
    candies = []
    if(type(result) == list):
        for item in result:
            zipped = zip(keys, item)
            candies.append(dict(zipped))
        return make_response(jsonify(candies), 200)
        # 200 code is good to get a get request
    else:
        return make_response(jsonify(candies), 500)


# ! CREATE NEW CANDY
@app.post('/api/candy')
def post_candy():
    name_input = request.json.get('candyName')
    description_input = request.json.get('candyDescription')
    if name_input == None:
        return "You must enter a name!"
    result = run_statement("CALL post_candy(?,?)", [name_input, description_input])
    if description_input == None:
        return "Your must enter a description!"
    if result == None:
        return "Post created Successfully"
    else:
        return "Something went wrong!"


# ! UPDATE CANDY
@app.patch('/api/candy')
def update_candy():
    id_input = request.json.get('candyId')
    description_input = request.json.get('candyDescription')
    if id_input == None:
        return "You must enter a valid candy ID!"
    result = run_statement("CALL update_candy(?,?)", [id_input, description_input])
    if description_input == None:
        return "Your must enter a description!"
    if result == None:
        return "Post updated Successfully"
    else:
        return "Something went wrong!"


    
# ! DELETE CANDY
@app.delete('/api/candy')
def delete_candy():
    id_input = request.json.get('candyId')
    if id_input == None:
        return "You must enter a valid candy ID!"
    result = run_statement("CALL delete_candy(?)", [id_input])
    if result == None:
        return make_response(jsonify("Post deleted Successfully"),200)
    else:
        return make_response(jsonify("Something went wrong!"), 500)

app.run(debug = True)