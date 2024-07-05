# #!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    bakeries_data = [bakery.to_dict() for bakery in bakeries]
    return make_response(jsonify(bakeries_data), 200)

@app.route('/bakeries/<int:id>')
def get_bakery(id):
    bakery = Bakery.query.get(id)
    if bakery:
        bakery_data = bakery.to_dict()
        bakery_data['baked_goods'] = [bg.to_dict() for bg in bakery.baked_goods]
        return make_response(jsonify(bakery_data), 200)
    return make_response(jsonify({"error": "Bakery not found"}), 404)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_data = [bg.to_dict() for bg in baked_goods]
    return make_response(jsonify(baked_goods_data), 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if baked_good:
        return make_response(jsonify(baked_good.to_dict()), 200)
    return make_response(jsonify({}), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)