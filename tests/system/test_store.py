from models.store import StoreModel
from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test')

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'id': 1, 'name': 'test', 'items': []}, json.loads(response.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test576')
                response = client.post('/store/test576')

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': "A store with name 'test576' already exists."}, json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test123')
                response = client.delete('/store/test123')

                self.assertEqual(response.status_code, 200)
                self.assertIsNone(StoreModel.find_by_name('test123'))
                self.assertDictEqual({'message': 'Store deleted'}, json.loads(response.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test124')
                response = client.get('/store/test124')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'id': 1, 'name': 'test124', 'items': []}, json.loads(response.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/test125')

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'},
                                     json.loads(response.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test134')
                client.post('/item/test_item', data={'price': 13.44, 'store_id': 1})

                response = client.get('/store/test134')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'id': 1, 'name': 'test134', 'items': [
                    {'name': 'test_item', 'price': 13.44}]},
                                     json.loads(response.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                for i in range(0, 5):
                    client.post(f'/store/{"test_"+str(i)}')
                response = client.get('/stores')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'stores': [{'id': 1, 'name': 'test_0', 'items': []},
                                                 {'id': 2, 'name': 'test_1', 'items': []},
                                                 {'id': 3, 'name': 'test_2', 'items': []},
                                                 {'id': 4, 'name': 'test_3', 'items': []},
                                                 {'id': 5, 'name': 'test_4', 'items': []}
                                                 ]
                                      },
                                     json.loads(response.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                for i in range(0, 5):
                    client.post(f'/store/{"test_" + str(i)}')
                    client.post(f'/item/{"test_item_" + str(i)}', data={'price': 13.44, 'store_id': i + 1})
                response = client.get('/stores')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'stores': [{'id': 1, 'name': 'test_0', 'items': [{'name': 'test_item_0', 'price': 13.44}]},
                                                 {'id': 2, 'name': 'test_1', 'items': [{'name': 'test_item_1', 'price': 13.44}]},
                                                 {'id': 3, 'name': 'test_2', 'items': [{'name': 'test_item_2', 'price': 13.44}]},
                                                 {'id': 4, 'name': 'test_3', 'items': [{'name': 'test_item_3', 'price': 13.44}]},
                                                 {'id': 5, 'name': 'test_4', 'items': [{'name': 'test_item_4', 'price': 13.44}]}
                                                 ]
                                      },
                                     json.loads(response.data))

