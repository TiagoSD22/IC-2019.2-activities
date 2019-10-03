from flask import Flask, request, jsonify, json
from flask_cors import CORS, cross_origin
import application, numpy

app = Flask(__name__)
CORS(app)


@app.route('/solve', methods=["POST"])
@cross_origin()
def process():
    data = numpy.asarray(request.get_json())
    application.run(data)

    return jsonify(data)


if __name__ == '__main__':
    app.run()
