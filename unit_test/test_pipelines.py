from unittest import TestCase
from douban.pipelines import MongodbPipeline



class TestMongodbPipeline(TestCase):
    mongodbPipeline = MongodbPipeline(mongo_url='mongodb://localhost:27017/', mongo_db='test', mongo_col='test')

    def test_process_item(self):
        item = {'test_key': 'test_value'}
        self.mongodbPipeline.process_item(item)
        self.assertTrue(self.mongodbPipeline.db['test'].find_one() is not None)
