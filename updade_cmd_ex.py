from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

#connects to database

engine=create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession=sessionmaker(bind=engine)

session=DBSession()

#select and update price of all veggie burguers

veggieBurgers =  session.query(MenuItem).filter_by(name = 'Veggie Burger')
for veggieBurger in veggieBurgers:
    print(veggieBurger.id)
    print(veggieBurger.price)
    print(veggieBurger.restaurant.name)

# select only the one with id of 20 

VeggiePandaGarden=session.query(MenuItem).filter_by(id=20).one()

print(VeggiePandaGarden.price)

#update price

VeggiePandaGarden.price='$2.99'

session.add(VeggiePandaGarden)
session.commit()

# update all prices 

for veggieBurger in veggieBurgers:
        if veggieBurger.price!='$2.99':
            veggieBurger.price='$2.99'
            session.add(veggieBurger)
            session.commit()
        


