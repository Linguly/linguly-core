# DB Proxy

Here we are mainly trying to build a data access abstraction layer configurable via the config.yaml file and later in the Linguly Lab.

In order to do so, we are providing a mongo db like interface and behind be able to use SQL based Query Builders to support rest of the DBs.

To build a comprehensive universal query layer we will waste a lot of time and there is no option available currently. Therefore, here we only focus on the required scope to be supported for the query type and DB types that are so far needed.
In addition, we will try to use the available maintained packages as much as possible.

> With this approach we are sacrificing maximum efficiency by providing more flexibility of changes and modifications in future.

Here is an overview of how it will look like at the end (examples provided by ChatGPT):

- Our Query Object Format (e.g., Mongo-style)
```python
query = {"name": "Alice", "age": {"$gte": 30}}
```

- Translator to Target ORM
    - For MongoDB, pass it directly to find()
    - For SQLAlchemy, translate it into SQLAlchemy filters:

```python
def translate_to_sqlalchemy(query):
    filters = []
    for key, value in query.items():
        if isinstance(value, dict) and "$gte" in value:
            filters.append(getattr(UserModel, key) >= value["$gte"])
        else:
            filters.append(getattr(UserModel, key) == value)
    return filters
```

- DB:
    > **Note:** in the actual development the logic is in each class separately

```python
class DB:
    ...
    def find(self, collection, query):
        if self.db_type == 'mongo':
            mongo_collection = db[collection]
            return mongo_collection.find(query)
        elif self.db_type == 'sql':
            filters = translate_to_sqlalchemy(query)
            UserModel = model[collection]
            return db_session.query(UserModel).filter(*filters).all()
```
