from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza',overlaps="restaurant_pizzas")
    
    
class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'
   
    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Define the relationship to the Pizza model with a different back reference name
    pizza = db.relationship('Pizza', backref='restaurant_pizza')
    restaurant = db.relationship('Restaurant', backref='restaurant_pizza')

    @validates("price")
    def validate_price(self, key, value):
        if not (1 <= value <= 30):
          raise ValueError("Price must be between 1 and 30")
        return value
class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'
   
    
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String,unique=True, nullable=False)
    address=db.Column(db.String)
    
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant',overlaps="restaurant_pizza")
    @validates("name")
    def validate_name(self,key,name):
        if name and len(name)>50:
            raise ValueError("name must be less than 50 words in length")