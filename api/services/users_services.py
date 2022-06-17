from sqlalchemy.orm import Session
# utils
from api.utils import encrypt
# schemas
from api.schemas.users_schemas import UserCreate
from api.schemas.tasks_schemas import TaskCreate, TaskUpdate
# models
from api.models.users_models import User
from api.models.tasks_models import Task


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 0):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    hashed_password = encrypt.encrypt_password(user.password)

    new_user = User(
        username=user.username, password=hashed_password, fullname=user.fullname)

    # save in database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_user_tasks(db: Session, user_id: int):
    return db.query(Task).filter(Task.owner_id == user_id).all()


def get_user_task(db: Session, user_id: int, task_id: int):
    return db.query(Task).filter(Task.owner_id == user_id).filter(Task.id == task_id).first()


def create_user_task(db: Session, task: TaskCreate, user_id: int):
    new_task = Task(**task.dict(), owner_id=user_id)

    # save in database
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def update_user_task(db: Session, user_id: int, task_id: int, task: TaskUpdate):
    if task.title is None and task.body is None:
        return 0
    elif task.title and task.body is None:
        task_update = db.query(Task)\
            .filter(Task.owner_id == user_id).filter(Task.id == task_id).update({"title": task.title})
    elif task.title is None and task.body:
        task_update = db.query(Task)\
            .filter(Task.owner_id == user_id).filter(Task.id == task_id).update({"body": task.body})
    else:
        task_update = db.query(Task)\
            .filter(Task.owner_id == user_id).filter(Task.id == task_id).update(task.dict())

    # commit current transaction in database
    db.commit()

    return task_update


def delete_user_task(db: Session, user_id: int, task_id: int):
    task_removed = db.query(Task).filter(Task.owner_id == user_id).filter(Task.id == task_id).delete()

    # commit current transaction in database
    db.commit()

    return task_removed
