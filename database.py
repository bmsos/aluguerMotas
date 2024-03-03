from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

connection_string = "mysql+mysqlconnector://root:@localhost:3306/aluguer_motas"
engine = create_engine(connection_string, echo=True)
Session = sessionmaker(bind=engine)
session = Session()