from fastapi import FastAPI, Request, HTTPException, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from typing import Annotated, List

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)
templates = Jinja2Templates(directory="templates")

users = []

class User(BaseModel):
    id: int
    age: int
    username: str

# Напишите новый запрос по маршруту '/':  +++++++++++++++++++++++ NEW
# Получение списка пользователей
@app.get("/", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

# Данные пользователя +++++++++++++++++++++++++++++++++++++++++++ NEW
@app.get('/user/{user_id}', response_class=HTMLResponse)
def read_user(
        request: Request,
        user_id: int = Path(..., title="ID пользователя", ge=1)
):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail="User was not found")


# POST
# Добавление пользователя в список
# все делается с подсказками и примерами
# Чтобы было однообразие - запросы и сообщения на одном языке
@app.post("/user/{username}/{age}")
async def add_user(
        username: Annotated[
            str,
            Path(title='Enter username', min_length=5, max_length=20, example='UrbanUser')
        ],
        age: Annotated[
            int,
            Path(title='Enter age', ge=0, le=120, example=24)
        ]
):
    if len(users):
        # new_user_id = len(users)
        new_user_id = users[-1].id + 1
    else:
        new_user_id = 1

    # Новый объект класса Users - он же новый пользователь
    new_user = User(id=new_user_id, username=username, age=age)
    users.append(new_user)
    return new_user

# PUT
# обновить данные о пользователе
@app.put('/user/{user_id}/{username}/{age}')
async def update_user(
        user_id: Annotated[
            int,
            Path(title='Enter new user ID', ge=1)
        ],
        username: Annotated[
            str,
            Path(title='Enter new username', min_length=5, max_length=20, example='UrbanProfi')
        ],
        age: Annotated[
            int,
            Path(title='Enter age', ge=0, le=120, example=28)
        ]
):
    for upd_user in users:
        if upd_user.id == user_id:
            upd_user.username = username
            upd_user.age = age
            return upd_user
    # Если пользователь не найден, выбрасываем исключение
    raise HTTPException(status_code=404, detail="User was not found")


# DELETE
# delete запрос по маршруту '/user/{user_id}', который удаляет из словаря users по ключу user_id пару
@app.delete('/user/{user_id}')
async def delete_user(
        user_id: Annotated[
            int,
            Path(title='Enter user ID ', example='2')
        ]
):
    for index, user in enumerate(users):
        if user.id == user_id:
            deleted_user = users.pop(index)
            return deleted_user
    # Если пользователь не найден, выбрасываем исключение
    raise HTTPException(status_code=404, detail="User was not found")

