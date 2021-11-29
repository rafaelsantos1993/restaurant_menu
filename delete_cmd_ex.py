from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

#connect to DB

engine=create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBsession=sessionmaker(bind=engine)

session=DBsession()

#select and delete all spinach ice cream 

spinach = session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()
print(spinach.restaurant.name, '\n')
session.delete(spinach)
session.commit()

#verify
spinach = session.query(MenuItem).filter_by(name='Spinach Ice Cream').one()


