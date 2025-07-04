from http import HTTPStatus
from fastapi_proj.schemas.user_schemas import UserPublic


def test_root_return_ola_mundo(client):
    response = client.get('/')

    assert response.json() == {'message': 'Olá mundo!'}
    assert response.status_code == HTTPStatus.OK


def test_register_user(client):
    response = client.post(
        '/user/',
        json={'username': 'teste', 'email': 'test@example.com', 'password': 'segredo'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'teste',
        'email': 'test@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/user/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/user/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user):
    response = client.get(f'/user/{user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_read_user_not_found(client):
    response = client.get('/user/100000')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user):
    response = client.put(
        '/user/1',
        json={
            'username': 'teste1',
            'email': 'test1@example.com',
            'password': 'segredo1',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'teste1',
        'email': 'test1@example.com',
        'id': 1,
    }


def test_update_user_not_found(client):
    response = client.put(
        '/user/100000',
        json={
            'username': 'teste1',
            'email': 'test1@example.com',
            'password': 'segredo1',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('/user/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/user/100000')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_interidity_error(client, user):
    client.post(
        '/user/',
        json={
            'username': 'error_update',
            'email': 'error_update@example.com',
            'password': 'segredo',
        },
    )

    response_update = client.put(
        f'/user/{user.id}',
        json={
            'username': 'error_update',
            'email': 'error_update@example.com',
            'password': 'segredo',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {'detail': 'User name or email already exists'}
