from http import HTTPStatus

from fastapi import FastAPI

from fastapi_proj.routers import auth, todos, users

app = FastAPI(title='Test Infog')

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)


@app.get('/', status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Olá mundo!'}
