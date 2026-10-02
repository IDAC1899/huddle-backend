from models.user import UserModel

def create_test_users():
    user1 = UserModel(username="isa_aldaaysi", email="isa@email.com")
    user1.set_password("123")
    user2 = UserModel(username="test1", email="test1@email.com")
    user2.set_password("123")
    user3 = UserModel(username="test2", email="test2@email.com")
    user3.set_password("123")
    user4 = UserModel(username="test3", email="test3@email.com")
    user4.set_password("123")
    user5 = UserModel(username="test4", email="test4@email.com")
    user5.set_password("123")

    return [user1, user2, user3, user4, user5]

user_list = create_test_users()