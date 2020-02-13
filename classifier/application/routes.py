from flask import Flask, request,jsonify
from application import app
from spam_classifier import classify

@app.route('/')
def hello_world():
    return 'Hello, Dummy!'


@app.route('/hello_user', methods=['POST'])
def hello_user():
    data = request.json
    user = data['user']
    return f'hello {user}'

@app.route('/get_number', methods=['POST'])
def get_number():
    data = request.json
    number = float(data['number'])
    return f'{number+1}'

@app.route('/classify_text', methods=['POST'])
def classify_text():
    data = request.json
    text = data['text']
    if text is None:
       params = ', '.join(data.keys()) 

       return jsonify({'message': f'Parametr "{params}" is invalid'}), 400 
    else:
       result = classify(text)
       return jsonify({'result': result})
