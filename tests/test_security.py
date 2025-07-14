from fastapi_proj.security import create_access_token, SECRET_KEY, ALGORITHM

from jwt import decode


def test_jwt():
    data = {'test': 'test'}

    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=ALGORITHM)

    assert decoded['test'] == data['test']
    assert 'exp' in decoded
