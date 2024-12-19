from fastapi import FastAPI, Path
from typing import Annotated
import uvicorn

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}


@app.get('/', summary='Список пользователей', tags=['Пользователи'])
async def get_users():
    return users


@app.post('/user/{username}/{age}', summary='Добавить пользователя', tags=['Пользователи'])
async def create_user(username: Annotated[str, Path(min_length=3, max_length=20)],
                      age: Annotated[int, Path(ge=14, le=30)]) -> str:
    user_id = int(max(users.keys(), default=0)) + 1
    users[str(user_id)] = f"Имя: {username}, возраст: {age}"
    return f"User {user_id} is registered"


@app.put('/user/{user_id}/{username}/{age}', summary='Изменить пользователя', tags=['Пользователи'])
async def update_user(user_id: Annotated[int, Path(gt=0, le=10)],
                      username: Annotated[str, Path(min_length=3, max_length=20)],
                      age: Annotated[int, Path(ge=14, le=30)]) -> str:
    if str(user_id) in users.keys():
        users[str(user_id)] = f"Имя: {username}, возраст: {age}"
        return f"User {user_id} is updated"
    else:
        return f"User {user_id} is not found"


@app.delete('/user/{user_id}', summary='Удалить пользователя', tags=['Пользователи'])
async def delete_user(user_id: Annotated[int, Path(gt=1, le=10)]):
    if str(user_id) in users.keys():
        del users[str(user_id)]
        return f"User {user_id} is deleted"
    else:
        return f"User {user_id} is not found"


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, port=8001)
