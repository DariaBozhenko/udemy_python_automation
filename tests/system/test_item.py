from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test')

                self.assertEqual(response.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test12', headers={'Authorization': self.access_token})

                self.assertEqual(response.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test34', 23.99, 1).save_to_db()
                response = client.get('/item/test34', headers={'Authorization': self.access_token})

                self.assertEqual(response.status_code, 200)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test124', 23.99, 1).save_to_db()
                response = client.delete('/item/test124')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'message': 'Item deleted'}, json.loads(response.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.post('/item/test24', data={'price': 22.99, 'store_id': 1})

                self.assertEqual(response.status_code, 201)
                self.assertDictEqual({'name': 'test24', 'price': 22.99}, json.loads(response.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test132', 18.99, 1).save_to_db()
                response = client.post('/item/test132', data={'price': 18.99, 'store_id': 1})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'An item with name \'test132\' already exists.'},
                                     json.loads(response.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.put('/item/test665', data={'price': 12.01, 'store_id': 1})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test665').price, 12.01)
                self.assertDictEqual({'name': 'test665', 'price': 12.01},
                                     json.loads(response.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test997', 23.99, 1).save_to_db()

                self.assertEqual(ItemModel.find_by_name('test997').price, 23.99)

                response = client.put('/item/test997', data={'price': 10.99, 'store_id': 1})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test997').price, 10.99)
                self.assertDictEqual({'name': 'test997', 'price': 10.99},
                                     json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                for i in range(0, 5):
                    client.post(f'/item/{"test_item_" + str(i)}', data={'price': 13.44, 'store_id': 1})
                response = client.get('/items')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'items': [{'name': 'test_item_0', 'price': 13.44},
                                                 {'name': 'test_item_1', 'price': 13.44},
                                                 {'name': 'test_item_2', 'price': 13.44},
                                                 {'name': 'test_item_3', 'price': 13.44},
                                                 {'name': 'test_item_4', 'price': 13.44}
                                                 ]
                                      },
                                     json.loads(response.data))

