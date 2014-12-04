# -*- coding: utf-8 -*-
import logging
import logging.config

__all__ = ['get_logger']


FILE_FORMATTER_PATTERN = '%(asctime)s %(levelname)s] %(message)s'

LOGGING = {
    'version': 1,
    'formatters': {
        'stream': {
            'format': '[%(asctime)s %(name)s %(levelname)s] %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(levelname)s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'stream'
        },
        'log_to_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'limn.log',
            'mode': 'a+',
            'formatter': 'file',
        },
        'logstash': {
            'level': 'INFO',
            'class': 'logstash.LogstashHandler',
            'host': 'localhost',
            'port': 5959,
            'version': 1,
            'message_type': 'logstash',
            'fqdn': False,
            'tags': ['tag1', 'tag2'],
        }
    },
    'loggers': {
        'limn_mobile': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False
        }
    }
}


def update_config(source_config, config):
    """
    Update source config dictionary with values from
    another config dictionary in a granular way, rather
    than only top level substituion.
    """
    for key, value in config.items():
        source_value = source_config.get(key)
        if not source_value:
            continue
        if isinstance(source_value, dict) and isinstance(value, dict):
            update_config(source_value, value)
        elif isinstance(source_value, list) and not isinstance(value, list):
            source_value.append(value)
        elif type(source_value) == type(value):
            source_config[key] = value


def update_logging_config(source_config, config, log_file_path,
                          logstash_endpoint):
    """
    Update logging config dict.
    """
    if config and isinstance(config, dict):
        update_config(source_config, config)
    if log_file_path:
        LOGGING['handlers']['log_to_file']['filename'] = log_file_path
        if 'log_to_file' not in LOGGING['loggers']['limn_mobile']['handlers']:
            LOGGING['loggers']['limn_mobile']['handlers'].append('log_to_file')
    if logstash_endpoint:
        host, port = logstash_endpoint.split(':')
        LOGGING['handlers']['logstash'].update({
            'host': host,
            'port': port
        })
        if 'logstash' not in LOGGING['loggers']['limn_mobile']['handlers']:
            LOGGING['loggers']['limn_mobile']['handlers'].append('logstash')


def get_logger(config={}, log_file_path=None,
               logstash_endpoint=None):
    """
    Get a logger instance for logging.
    """
    update_logging_config(LOGGING, config, log_file_path, logstash_endpoint)
    logging.config.dictConfig(LOGGING)
    logger = logging.getLogger('limn_mobile')
    return logger
