from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd

_db_uri = 'sqlite:///:memory:'
engine = create_engine(_db_uri, echo=True)
Session = sessionmaker(bind=engine)

Base = declarative_base(engine)

class MyTable(Base):
    __tablename__ = 'my_table'
    id = Column(Integer, primary_key=True)
    date = Column(String)
    name = Column(String)
    value = Column(Integer)

def _test():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = Session()

    def _add_test_data():
        rows = [
            MyTable(date="D1", name="A", value=2),
            MyTable(date="D1", name="B", value=3),
            MyTable(date="D2", name="A", value=3),
            MyTable(date="D2", name="C", value=1),
        ]
        session.add_all(rows)
        session.commit()

    # create test data
    _add_test_data()

    # use `sa` to query data from the database
    # q = session.query(MyTable)  # all columns
    q = session.query(MyTable.date, MyTable.name, MyTable.value)  # explicit

    # read data into pandas directly from the query `q`
    df = pd.read_sql(q.statement, q.session.bind)
    print(df)

    # pivot the results
    df_pivot = df.pivot(index="date", columns="name", values="value")
    print(df_pivot)


if __name__ == '__main__':
    _test()