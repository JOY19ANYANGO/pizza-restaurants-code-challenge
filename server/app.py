#!/usr/bin/env python3

#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound

from models import db, Restaurant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Restaurants(Resource):

    def get(self):
        restaurants = []
        for restaurant  in Restaurant.query.all():
            restaurant_dict={
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address
            }
            restaurants.append(restaurant_dict)
        return make_response(jsonify(restaurants), 200)

    # def post(self):
    #     data = request.get_json()

    #     new_plant = Plant(
    #         name=data['name'],
    #         image=data['image'],
    #         price=data['price'],
    #     )

    #     db.session.add(new_plant)
    #     db.session.commit()

    #     return make_response(new_plant.to_dict(), 201)


api.add_resource(Restaurants, '/restaurants')


class RestaurantByID(Resource):

    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            restaurant_dict=restaurant.to_dict()
            return make_response(jsonify(restaurant_dict), 200)
        else:
            return make_response(jsonify({"error": "Restaurant not found"}), 404)

#     def patch(self,id):
#         plant = Plant.query.filter_by(id=id).first()
#         if plant:
#             for attr in request.form:
#                 setattr(plant, attr, request.form.get(attr))
#             setattr(plant, "is_in_stock", False)
#             db.session.add(plant)
#             db.session.commit()
#             plant_dict = plant.to_dict()
#             return make_response(plant_dict, 200)
#         else:
#             raise NotFound

    def delete(self,id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return make_response("", 204)
        else:
            return make_response(jsonify({"error": "Restaurant not found"}), 404)



api.add_resource(RestaurantByID, '/restaurants/<int:id>')

@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        "Not Found: The requested resource does not exist.",
        404
    )
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)