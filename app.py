from urllib import request

from flask import Flask, request, jsonify

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes in your Flask app


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'
databases = {}

@app.route('/add_item', methods = ['POST'])
def add_item():
    """location = request.args.get('location')
    name = request.args.get('name')
    qty = request.args.get('quantity')

    try:
        databases[location].add_item(location, name, qty)
        return jsonify({'message': 'Item added successfully'}, 200)
    except:
        return jsonify({'error': 'Something wend wrong, please try again'}), 400
    """
    print(request.form)
    received_data = request.data.decode('utf-8')
    print("Request JSON Data:", received_data)
    return jsonify({'were here' : 1})
@app.route('/update_item', methods=['POST'])
def update_item():
    # Extracting values from the URL query string (GET parameters)
    item_id = request.args.get('item_id')
    location = request.args.get('location')
    quantity = request.args.get('quantity')
    user = request.args.get('user')
    try:
        return jsonify({'message': 'Item added successfully'}, 200)
    except:
        return jsonify({'error': 'Something wend wrong, please try again'}), 400

if __name__ == '__main__':
    app.run()
