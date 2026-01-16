from flask import Flask, request, jsonify
from ivr_logic import ivr_routing
from queue_logic import get_all_queues_status

app = Flask(__name__)

@app.route('/ivr', methods=['POST'])
def ivr():
    data = request.json
    user_input = data.get('input')
    response = ivr_routing(user_input)
    return jsonify(response)

@app.route('/queues', methods=['GET'])
def queues():
    status = get_all_queues_status()
    return jsonify(status)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
