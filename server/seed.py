from random import randint, choice as rc
from faker import Faker
from app import app
from models import db, Pizza, RestaurantPizza, Restaurant
import random
fake = Faker()

with app.app_context():
    # Create and add fake restaurants
    restaurants = [
        Restaurant(
            name=fake.company(),
            address=fake.address()
        )
        for i in range(10)
    ]
    db.session.add_all(restaurants)  # Use db.session.add_all() to add the list
    db.session.commit()

    # Create and add fake pizzas
    pizzas = [
        Pizza(
            name=fake.word(),
            ingredients=', '.join(fake.words())
        )
        for i in range(10)
    ]
    db.session.add_all(pizzas)  # Use db.session.add_all() to add the list
    db.session.commit()

    # Create restaurant-pizza relationships
    restaurant_pizzas = [
        RestaurantPizza(
            pizza_id=random.choice(pizzas).id,
            restaurant_id=random.choice(restaurants).id,
            price=random.randint(1, 30)
        )
        for i in range(10)
    ]
    db.session.add_all(restaurant_pizzas)  # Use db.session.add_all() to add the list
    db.session.commit()
