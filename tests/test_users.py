# from fastapi.testclient import TestClient
# from main import app

# client = TestClient(app)

# def test_get_all_users():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert len(response.json()) >= 0

# def test_create_new_user():
#     new_user = {
#         "username": "vandoe",
#         "password": "secret",
#         "email": "ben@example.com"
#     }
#     response = client.post("/users/create", json=new_user)
#     assert response.status_code == 200
#     assert response.json()['username'] == 'vandoe'

# def test_get_user():
#     response = client.get("/users/vandoe")
#     assert response.status_code == 200
#     assert response.json()['username'] == 'vandoe'

# def test_update_user_details():
#     updated_user = {
#         "password": "newpassword",
#         "old_password":"secret",
#         "email": "ven_updated@example.com"
#     }
#     response = client.put("/users/update/vandoe", json=updated_user)
#     assert response.status_code == 200
#     assert response.json()['email'] == 'ven_updated@example.com'