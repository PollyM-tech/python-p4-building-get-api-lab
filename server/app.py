#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(jsonify(all_bakeries), 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery:
        return make_response(jsonify(bakery.to_dict()), 200)
    else:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    goods = [bg.to_dict() for bg in BakedGood.query.order_by(BakedGood.price.desc()).all()]
    return make_response(jsonify(goods), 200)
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    bg = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if bg:
        return make_response(jsonify(bg.to_dict()), 200)
    else:
        return make_response(jsonify({'error': 'No baked goods found'}), 404)
if __name__ == '__main__':
    app.run(port=5555, debug=True)
