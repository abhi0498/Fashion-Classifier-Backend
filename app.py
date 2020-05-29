from flask import Flask, render_template, request, jsonify
from predict import predict_from_file, predict_from_url
from getProducts import get_all_products
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/api/image-search', methods=['GET', 'POST'])
@cross_origin()
def home():
    print(f"[POST] {request.files['image']}")

    file = request.files['image']
    file.save('./temp/' + file.filename)
    print(file.filename)

    pred = predict_from_file('./temp/'+file.filename)
    # @TODO change arg to ' '.join(pred)
    products = {}
    products = get_all_products(
        pred['gender'][0][0] + ' ' + pred['colour']
        [0][0] + ' ' + pred['article'][0][0])
    return jsonify({'products': products, 'results': pred})


@app.route('/api/search', methods=['GET'])
@cross_origin()
def search():
    term = request.args.get('term')
    print('[POST]', term)
    products = get_all_products(term)
    return jsonify({'products': products})


@app.route('/api/image-search-url', methods=['POST'])
@cross_origin()
def url_search():
    term = request.json['url']
    pred = predict_from_url(term)
    # @TODO change arg to ' '.join(pred)
    products = {}
    # pred = {}
    print('[Prediction]'+pred['gender'][0][0] + ' ' + pred['colour']
          [0][0] + ' ' + pred['article'][0][0])
    products = get_all_products(
        pred['gender'][0][0] + ' ' + pred['colour']
        [0][0] + ' ' + pred['article'][0][0])
    return jsonify({'products': products, 'results': pred})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
