import pytest
from sqlalchemy import *  # noqa

from sqla_wrapper import SQLAlchemy


def test_repr(memdb):
    assert memdb.url in str(memdb)


def test_setup_with_params_full():
    db = SQLAlchemy(
        dialect="postgresql+psycopg2",
        user="scott",
        password="tiger",
        host="localhost",
        port=123,
        name="test",
    )
    assert db.url == "postgresql+psycopg2://scott:tiger@localhost:123/test"


def test_setup_with_some_params():
    db = SQLAlchemy(
        dialect="postgresql",
        user="postgres",
        host="localhost",
        name="test",
    )
    assert db.url == "postgresql://postgres@localhost/test"


def test_setup_with_password():
    db = SQLAlchemy(
        dialect="postgresql",
        user="postgres",
        password="postgres",
        name="dbtest",
    )
    assert db.url == "postgresql://postgres:postgres@127.0.0.1/dbtest"


def test_setup_with_params_minimal():
    db = SQLAlchemy(dialect="sqlite")
    assert db.url == "sqlite://"


def test_setup_with_sqlite_path():
    db = SQLAlchemy(dialect="sqlite", name="relpath/to/database.db")
    assert db.url == "sqlite:///relpath/to/database.db"


def test_setup_with_driver_options():
    name = (
        "file:path/to/database.db?"
        "check_same_thread=true&timeout=10&mode=ro&nolock=1&uri=true"
    )
    db = SQLAlchemy(dialect="sqlite+pysqlite", name=name)
    assert db.url == f"sqlite+pysqlite:///{name}"


def test_drop_all(memdb):
    class ToDo(memdb.Model):
        __tablename__ = "todos"
        id = Column(Integer, primary_key=True)

    memdb.create_all()
    memdb.drop_all()

    with pytest.raises(Exception):
        with memdb.Session() as session:
            session.execute(select(ToDo)).all()


def test_single_table_inhertance(memdb):
    class Person(memdb.Model):
        __tablename__ = "persons"
        id = Column(Integer, primary_key=True)
        type = Column(String(50))
        __mapper_args__ = {
            "polymorphic_identity": "person",
            "polymorphic_on": type,
        }

    class Engineer(Person):
        engineer_name = Column(String(30))
        __mapper_args__ = {"polymorphic_identity": "engineer"}

    class Manager(Person):
        manager_name = Column(String(30))
        __mapper_args__ = {"polymorphic_identity": "manager"}

    memdb.create_all()

    with memdb.Session() as dbs:
        dbs.create(Engineer, engineer_name="Bob")
        dbs.commit()

        obj = dbs.first(Engineer)
        assert obj.engineer_name == "Bob"
        assert obj.type == "engineer"
