from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import Base, Item
from sqlalchemy.exc import OperationalError
from sqlalchemy import inspect, Engine, text

"""dialect+driver://username:password@host:port/database"""


def get_engine(
    username="",
    password="",
    hostname="localhost",
    port="3306",
    database_name="",
    use_memory=False,
):
    if not use_memory:
        url = f"mysql+mysqlconnector://{username}:{password}@{hostname}:{port}"
        engine = create_engine(url, echo=False)
        with engine.connect() as conn:
            try:
                conn.execute(text(f"USE {database_name}"))
            except Exception as ex:
                print(f"{database_name} does not exists. Will be created")
                conn.execute(
                    text(f"CREATE DATABASE IF NOT EXISTS {database_name} ")
                )  # create db

        url = f"mysql+mysqlconnector://{username}:{password}@{hostname}:{port}/{database_name}"
    else:
        url = "sqlite:///:memory:"
    engine = create_engine(url, echo=False)

    Base.metadata.create_all(engine)
    return engine


# class Database:
#     def __init__(self, username="", password="", hostname="", port="3306", database_name="", use_memory=False):
#         if not use_memory:
#             url = f"mysql+mysqlconnector://{username}:{password}@{hostname}:{port}"
#             self.engine = create_engine(url, echo=True)
#             with self.engine.connect() as conn:
#                 try:
#                     conn.execute(f"USE {database_name}")
#                 except OperationalError as ex:
#                     print(f"{database_name} does not exists. Will be created")
#                     conn.execute(f"CREATE DATABASE {database_name} IF NOT EXISTS")  # create db

#             url = f"mysql+mysqlconnector://{username}:{password}@{hostname}:{port}/{database_name}"
#         else:
#             url = "sqlite:///:memory:"
#         self.engine = create_engine(url, echo=True)

#         Base.metadata.create_all(self.engine)
#         Session =
#         self.session = Session()


#     def get_db(self):
#         return self


class ItemOperation:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine)
        print(engine)
        print(self.Session)
        # print(database.engine.table)/
        print(inspect(self.engine.engine).get_table_names())
        pass

    def check_exists_with_name(self, name):
        with self.Session() as session:
            item = session.query(Item).filter_by(name=name).first()
            print(item)
            if not item:
                print(f"item called {name} does not exists!")
                return True
            else:
                print(f"item called {name} exists!")
                return False

    def check_exists_with_id(self, id: int):
        with self.Session() as session:
            item = session.query(Item).filter_by(id=id).first()
            print("qweqwe", item)
            if not item:
                print(f"item with id = {id} does not exists!")
                return False
            else:
                print(f"item with id = {id} exists!")
                return True

    def add_item(self, *, name, description, price, count):  # C
        try:
            with self.Session() as session:
                new_item = Item(
                    name=name, description=description, price=price, count=count
                )
                print("Adding items")
                session.add(new_item)
                session.commit()
        except Exception as e:
            print("Exception: ", e)
            pass

    def delete_item(self, id: int):  # R
        with self.Session() as session:
            item = session.query(Item).filter_by(id=id).first()
            print(item)
            if not item:
                print(f"item with id = {id} does not exists!")
                return False
            else:
                session.delete(item)
                session.commit()
                print(f"item with id = {id} deleted!")
                return True

    def edit_item(self, id: int, updated_data: dict()):  # U
        with self.Session() as session:
            item = session.query(Item).filter_by(id=id).first()
            if not item:
                print(f"item with id = {id} does not exists!")
                return False
            item.name = updated_data["name"]
            item.description = updated_data["description"]
            item.price = updated_data["price"]
            item.count = updated_data["count"]
            session.commit()
            print(f"item with id = {id} updated!")
            return True

    def query_item_using_id(self, id: int):
        with self.Session() as session:
            item = session.query(Item).filter_by(id=id).first()
            return {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "count": item.count,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
            }

    def query_item_using_string(self, query: str = ""):  # D
        with self.Session() as session:
            items = session.query(Item).all()
            print("querying items")
            if query.strip() == "":
                item_lst = [
                    {
                        "id": item.id,
                        "name": item.name,
                        "description": item.description,
                        "price": item.price,
                        "count": item.count,
                        "created_at": item.created_at,
                        "updated_at": item.updated_at,
                    }
                    for item in items
                ]
            else:
                item_lst = [
                    {
                        "id": item.id,
                        "name": item.name,
                        "description": item.description,
                        "price": item.price,
                        "count": item.count,
                        "created_at": item.created_at,
                        "updated_at": item.updated_at,
                    }
                    for item in items
                    if query.strip() in item.name.lower()
                    or (item.description and query.strip() in item.description.lower())
                ]
            return item_lst
