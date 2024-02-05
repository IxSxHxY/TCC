from database import get_engine, ItemOperation
username="root"
password=""
hostname="localhost"
port="3306"
database_name="TCC"

database = get_engine(
    username=username,
    password=password,
    hostname=hostname,
    port=port,
    database_name=database_name,
    use_memory=False)
item_ops = ItemOperation(database)
item_ops.add_item(name=,
                  description=,
                  price=,
                  count=)
item_ops.is_unique("Ivanssss")
print('12213123213')
item_ops.query_item()