from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

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
    
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza')
    
class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'
   
    
    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    resaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    price=db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    @validates("price")
    def validate_price(self, key, value):
        if not (1 <= value <= 30):
          raise ValueError("Price must be between 1 and 30")
        return value
class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'
   
    
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String,unique=True,nullable=False)
    address=db.Column(db.String)
    
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant')
    @validate("name")
    def validate_name(self,key,name):
        if name and len(name)>50:
            raise ValueError("name must be less than 50 words in length")