# -*- coding: utf-8 -*-
import unittest
import logging
import copy
from logger import update_config, update_logging_config, get_logger


class TestUpdateConfig(unittest.TestCase):

    def test_success(self):
        SOURCE_CONFIG = {
            'a': 1,
            'b': {
                'b1': ['blah']
            },
            'c': ['foo']
        }

        CONFIG = {
            'a': 2,
            'b': {
                'b1': 'foobar',
                'b2': 'whatever'
            },
            'c': [1, 2]
        }
        UPDATED_CONFIG = {
            'a': 2,
            'b': {
                'b1': ['blah', 'foobar']
            },
            'c': [1, 2]
        }
        update_config(SOURCE_CONFIG, CONFIG)
        self.assertEqual(SOURCE_CONFIG, UPDATED_CONFIG)


class TestUpdateLoggingConfig(unittest.TestCase):

    def test_success(self):
        from logger import LOGGING
        UPDATED_LOGGING = copy.deepcopy(LOGGING)
        UPDATED_LOGGING['loggers']['limn_mobile']['handlers'] = [
            'console', 'logstash', 'log_to_file']
        UPDATED_LOGGING['handlers']['log_to_file']['filename'] = 'test.log'
        update_logging_config(LOGGING, {
            'loggers': {
                'limn_mobile': {
                    'handlers': ['console', 'logstash']
                }
            }
        }, 'test.log', None)
        self.assertEqual(LOGGING, UPDATED_LOGGING)


class TestGetLogger(unittest.TestCase):

    def test_success(self):
        logger = get_logger(
            config={
                'loggers': {
                    'limn_mobile': {
                        'handlers': ['console', 'logstash']
                    }
                }
            },
            log_file_path='test.log')
        self.assertTrue(isinstance(logger, logging.Logger))
        self.assertEqual(len(logger.handlers), 3)
