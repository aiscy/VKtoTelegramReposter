import logging

from secret_config import keys

LOGGING_LEVEL=logging.DEBUG

conf = dict(
    HOST='0.0.0.0',
    PORT='80',
    KEYS=keys,
    LOGGING_CONF=dict(
            version=1,
            disable_existing_loggers=False,
            formatters={
                'f': {'format':
                          '%(levelname)s:%(name)s: %(message)s (%(asctime)s; %(filename)s:%(lineno)d)'}
            },
            handlers={
                'console': {'class': 'logging.StreamHandler',
                            'formatter': 'f',
                            'level': LOGGING_LEVEL},

                'file': {'class': 'logging.handlers.RotatingFileHandler',
                         'filename': 'root.log',
                         'backupCount': 3,
                         'maxBytes': 10000000,
                         'encoding': 'utf8',
                         'formatter': 'f',
                         'level': LOGGING_LEVEL}
            },
            root={
                'handlers': ['console', 'file'],
                'level': LOGGING_LEVEL,
            }
    )

)
