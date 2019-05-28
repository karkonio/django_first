def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    assert 'Hello, World!' in response
