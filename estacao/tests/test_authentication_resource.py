import json
from estacao.blueprints.restapi.resources import UserResource
from flask_restful import Resource


class TestUserResource:
    def test_is_instance(self, user_resource):
        assert isinstance(user_resource, UserResource)
        assert isinstance(user_resource, Resource)

    def test_has_get_attribute(self):
        assert hasattr(UserResource, 'get')

    def test_get_return_users(self, user_resource, users):
        response = user_resource.get('login_test')
        users = json.loads(response.data)
        assert users.get('user').get('login') == 'login_test'











































