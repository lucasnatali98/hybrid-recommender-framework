import logging

from flask import Flask, json
from flask import request
from flask_cors import CORS, cross_origin
from task_executor import execute_task

app = Flask(__name__)
cors = CORS(app)
logging.getLogger('flask_cors').level = logging.DEBUG


@app.route('/check', methods=['GET'])
def hello():
    response = app.response_class(
        response="Server is running!",
        status=200,
        mimetype='text/plain'
    )
    return response


@cross_origin
@app.route('/run', methods=['POST'])
def post():
    task_info = request.get_json()
    task_output = execute_task(task_info)
    response = app.response_class(
        response=json.dumps(task_output),
        status=200,
        mimetype='application/json'
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
