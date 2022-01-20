import time
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship


MAX_GARAGE_SIZE = 10;

engine = create_engine('sqlite:///garage.db')

Base = declarative_base()
class Reciept(Base):
    __tablename__ = "garage"
    car_regno = Column(String,primary_key=True)
    car_type = Column(String)
    entry_time = Column(String)
    def __init__(self, car_regno,car_type,entry_time):
        self.car_regno = car_regno
        self.car_type = car_type
        self.entry_time = entry_time
    def __str__(self):
        return f"{self.car_regno} {self.car_type} {self.entry_time}"

Session = sessionmaker(engine)
Base.metadata.create_all(engine)
session = Session();

def truncate(n):
    """
      truncate n to 3 decimal points
    """
    return int(n * 1000) / 1000

def print_reciept():
    garage = session.query(Reciept).all()
    cars_in_garage = session.query(Reciept).count()
    if len(garage) >= MAX_GARAGE_SIZE:
        print("Info: Garage is at full capacity")
        return
    print("Parking Manager v1.0")
    print("All Cars: ")
    print("regno type entry_time")
    print("-----------------------")
    for reciept in garage:
        print(reciept)
    print("")
    print(f"Number of cars: {cars_in_garage}")
    reciept_type = input("Input Reciept Type[entry/exit]: ").lower();
    car_regno = input("Input Car Regno: ");
    if reciept_type == "entry":
        car_type = input("Input car type [small,regular,large]: "); #small -> 10rs/hr,regular ->20rs/hr,large ->30rs/hr
        if car_type not in ["small","regular","large"]:
            print("Error: Invalid car type")
            return
        entry_time = time.time()
        print(f"{car_regno} {car_type} {entry_time}")
        reciept = Reciept(car_regno,car_type,str(entry_time))
        try:
            session.add(reciept)
            session.commit()
        except:
            print("Error: Registration number already exists")
    elif reciept_type == "exit":
        reciept = session.query(Reciept).filter(Reciept.car_regno == car_regno).scalar()
        if reciept == None:
            print(f"No such car parked with regno {car_regno}")
            return
        print(reciept)
        time_spent = float(time.time()) - float(reciept.entry_time)
        time_spent = float(time_spent/3600)
        time_spent = truncate(time_spent)
        print("Time spent {:.3f} hrs".format(time_spent))
        price = 0
        if reciept.car_type == "small":
            price = time_spent * 10
        elif reciept.car_type == "regular":
            price = time_spent * 20
        else:
            price = time_spent * 30
        print("Total price for {:.3f} hrs: Rs{:.3f}".format(time_spent,price))
        session.delete(reciept)
        session.commit()
    else:
        print("Error: Invalid  Reciept Type")



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_reciept()
    session.close();

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
