from flask import Flask, render_template, request, jsonify
from predict import predict
from getProducts import get_all_products
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/api/image-search', methods=['GET', 'POST'])
@cross_origin()
def home():
    print(f"[POST] {request.data}")
    # f = request.data
    # with open('./temp/temp.jpg', 'wb') as file:
    #     file.write(f)
    # file = request.files['file']
    # file.save('./temp/' + file.filename)
    # print(file.filename)
    # pred = predict(file.filename)
    # @TODO change arg to ' '.join(pred)
    products = get_all_products('blue color men shirt')
    return jsonify({'products': products})


@app.route('/api/search', methods=['GET'])
@cross_origin()
def search():
    term = request.args.get('term')
    print(term)
    products = get_all_products(term)
    return jsonify({'products': products})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
