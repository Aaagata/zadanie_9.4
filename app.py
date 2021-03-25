from flask import Flask, jsonify
from models import costs
from flask import abort, make_response, request, render_template, redirect, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/costs/", methods=["GET"])
def costs_list_api():
    return jsonify(costs.all())

@app.route("/costs/<int:cost_id>", methods=["GET"])
def get_cost(cost_id):
    cost = costs.get(cost_id)
    if not cost:
        abort(404)
    return jsonify({"cost": cost})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.route("/costs/", methods=["POST"])
def create_cost():
    if not request.json or not 'amount' in request.json:
        abort(400)
    cost = {
        'id': costs.all()[-1]['id'] + 1,
        'amount': request.json['amount'],
        'description': request.json.get('description', ""),
        'done': False
    }
    costs.create(cost)
    return jsonify({'cost': cost}), 201

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

@app.route("/costs/<int:cost_id>", methods=['DELETE'])
def delete_cost(cost_id):
    result = costs.delete(cost_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/costs/<int:cost_id>", methods=["PUT"])
def update_cost(cost_id):
    cost = costs.get(cost_id)
    if not cost:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'amount' in data and not isinstance(data.get('amount'), int),
        'description' in data and not isinstance(data.get('description'), str),
        'done' in data and not isinstance(data.get('done'), bool)
    ]):
        abort(400)
    cost = {
        'amount': data.get('amount', cost['amount']),
        'description': data.get('description', cost['description']),
        'done': data.get('done', cost['done'])
    }
    costs.update(cost_id, cost)
    return jsonify({'cost': cost})

if __name__ == "__main__":
    app.run(debug=True)