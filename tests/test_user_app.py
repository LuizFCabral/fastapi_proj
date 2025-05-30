from http import HTTPStatus


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
    assert response.json() == {
        'users': [
            {
                'username': 'teste',
                'email': 'test@example.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
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


def test_delete_user(client): 
    response = client.delete('/user/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}
