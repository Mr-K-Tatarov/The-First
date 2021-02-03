from api.request import RequestCreateUserDto, RequestPatchUserDto
from db.database import DBSession
from db.exceptions import DBUserNotExists, DBUserExists
from db.models import DBUser


def create_user(
        session: DBSession, *, user: RequestCreateUserDto, hashed_password: bytes
) -> DBUser:
    new_user = DBUser(
        login=user.login,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
    )

    try:
        if get_user_by_login(session, login=new_user.login):
            raise DBUserExists(new_user.login)
    except DBUserNotExists:
        pass

    session.add_model(new_user)

    return new_user


def get_user_by_login(session: DBSession, *, login: str) -> DBUser:
    user = session.query(DBUser).filter(DBUser.login == login).first()
    if user is None:
        raise DBUserNotExists

    return user


def get_user_by_id(session: DBSession, *, user_id: int) -> DBUser:
    db_user = session.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise DBUserNotExists

    return db_user


def update_user(session: DBSession, user: RequestPatchUserDto, user_id: int) -> DBUser:
    db_user = get_user_by_id(session, user_id=user_id)

    for attr in user.fields:
        if hasattr(user, attr):
            value = getattr(user, attr)
            setattr(db_user, attr, value)

    return db_user


def delete_user(session: DBSession, user_id: int) -> DBUser:
    db_user = get_user_by_id(session, user_id=user_id)
    db_user.is_delete = True
    return db_user
