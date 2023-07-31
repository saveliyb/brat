from sqlalchemy.orm import Session

from server.models import Admin_DB
from server import pydantic_models
from server.CRUD.security import hash_password, generate_salt


def register_admin(db: Session, admin: pydantic_models.RegisterAdmin, who_create: str = None):
    salt = generate_salt()
    admin_hash_password = hash_password(password=admin.admin_password, salt=salt)
    new_admin = Admin_DB(admin_login=admin.admin_login,
                         admin_hash_password=admin_hash_password,
                         is_super_admin=admin.is_super_admin,
                         is_active=admin.is_active,
                         who_create=who_create,
                         salt=salt)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin


def get_admin_login(db: Session, admin_login: str):
    admin = db.query(Admin_DB).filter(Admin_DB.admin_login == admin_login)
    return admin.scalar()


def get_admin_id(db: Session, id_admin: int):
    admin = db.query(Admin_DB).filter(Admin_DB.id_admin == id_admin)
    return admin.scalar()


def set_active(db: Session, admin: pydantic_models.SetActiveAdmin):
    changeable_admin = db.query(Admin_DB).filter(Admin_DB.admin_login == admin.admin_login).update(
        {"is_active": admin.is_active}, synchronize_session=False)
    db.commit()
    return changeable_admin


def delete_admin(db: Session, admin: pydantic_models.DeleteAdmin):
    admin_to_delete = db.query(Admin_DB).filter(Admin_DB.admin_login == admin.bottom_admin_login).delete(synchronize_session=False)
    db.commit()
    return admin_to_delete


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
        # new_admin = pydantic_models.RegisterAdmin(admin_login="abcd",
        #                                           admin_password="123456789",
        #                                           is_super_admin=False,
        #                                           is_active=True)
        # register_admin(db=db, admin=new_admin, who_create="main_admin")
        # print("\t\t\t", get_admin_login(db=db, admin_login="abcd"), get_admin_login(db=db, admin_login="abcd").id_admin)
        # print("\t\t\t", get_admin_id(db=db, id_admin=1), get_admin_id(db=db, id_admin=1).admin_login)
        set_active(db=db, admin=pydantic_models.SetActiveAdmin(admin_login="abcd", is_active=True))
        # print(delete_admin(db=db, admin=pydantic_models.DeleteAdmin(bottom_admin_login="abcd")))