import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgis://localhost/pupa')
os.environ['OCD_DIVISION_CSV'] = os.environ.get('OCD_DIVISION_CSV', os.path.join(os.path.abspath(os.path.dirname(__file__)), 'scrapers/country-{}.csv'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "%(asctime)s %(levelname)s %(name)s: %(message)s",
            'datefmt': '%H:%M:%S'
        }
    },
    'handlers': {
        'default': {'level': 'DEBUG',
                    'class': 'logutils.testing.TestHandler',
                    'matcher': 'logutils.testing.Matcher',
                    'formatter': 'standard'},
    },
    'loggers': {
        '': {
            'handlers': ['default'], 'level': 'WARN', 'propagate': True  # DEBUG
        },
        'scrapelib': {
            'handlers': ['default'], 'level': 'WARN', 'propagate': False  # INFO
        },
        'requests': {
            'handlers': ['default'], 'level': 'WARN', 'propagate': False
        },
        'boto': {
            'handlers': ['default'], 'level': 'WARN', 'propagate': False
        },
    },
}
