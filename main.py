from fastapi import FastAPI, Depends, Header, status
# schemas
from api.schemas.tasks_schemas import TaskCreate, TaskUpdate
from api.schemas.auth_schemas import SigninBase, SignupBase
# services
from api.services import auth_services, users_services
# database
from database import engine, Base, SessionLocal
# sqlalchemy
from sqlalchemy.orm import Session

# create all tables
Base.metadata.create_all(bind=engine)


app = FastAPI()


# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/signin", status_code=status.HTTP_200_OK)
async def signin(credentials: SigninBase, db: Session = Depends(get_db)):
    user_token = auth_services.signin(db, credentials)

    return {"jwt": user_token}


@app.post("/api/signup", status_code=status.HTTP_201_CREATED)
async def signup(credentials: SignupBase, db: Session = Depends(get_db)):
    user_token = auth_services.signup(db, credentials)

    return {"jwt": user_token}


@app.get("/api/users/me")
async def get_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    user_id = auth_services.decode_auth_token(authorization)
    user_found = users_services.get_user(db, user_id)

    user_payload = {
        "id": user_found.id,
        "username": user_found.username,
        "fullname": user_found.fullname,
        "tasks": user_found.tasks,
        "is_active": user_found.is_active
    }

    return {"detail": "user found", "data": user_payload}


@app.get("/api/users/me/tasks")
async def get_user_tasks(authorization: str = Header(...), db: Session = Depends(get_db)):
    user_id = auth_services.decode_auth_token(authorization)
    tasks = users_services.get_user_tasks(db, user_id)

    return {"detail": "tasks found", "data": tasks}


@app.post("/api/users/me/tasks")
async def create_user_task(task: TaskCreate, authorization: str = Header(...), db: Session = Depends(get_db)):
    user_id = auth_services.decode_auth_token(authorization)
    task_created = users_services.create_user_task(db, task, user_id)

    return {"detail": "task created", "data": task_created}


@app.get("/api/users/me/tasks/{task_id}")
async def get_user_task(task_id: int, authorization: str = Header(...), db: Session = Depends(get_db)):
    user_id = auth_services.decode_auth_token(authorization)
    task_found = users_services.get_user_task(db, user_id, task_id)

    return {"detail": "task found", "data": task_found}


@app.put("/api/users/me/tasks/{task_id}")
async def update_user_task(task_id: int, task: TaskUpdate, authorization: str = Header(...), db: Session = Depends(get_db)):
    user_id = auth_services.decode_auth_token(authorization)
    task_update = users_services.update_user_task(db, user_id, task_id, task)

    return {"detail": "task updated", "updated": task_update}


@app.delete("/api/users/me/tasks/{task_id}")
async def delete_user_task(task_id: int, authorization: str = Header(...), db: Session = Depends(get_db)):
    user_id = auth_services.decode_auth_token(authorization)
    user_removed = users_services.delete_user_task(db, user_id, task_id)

    return {"detail": "task removed", "removed": user_removed}
