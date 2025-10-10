from http import HTTPStatus


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'test',
            'description': 'testing todo creation',
            'state': 'draft',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'title': 'test',
        'description': 'testing todo creation',
        'state': 'draft',
        'id': 1,
    }
