def test_hello(db, client, data):
    client.login(username='kira', password='testtest')
    response = client.get('/')
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    assert 'Hello, World!' in response
    assert 'kira' in response
