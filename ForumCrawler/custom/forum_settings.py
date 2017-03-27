# -*- coding: utf-8 -*-
import time

JOBDIR = 'job_1point3acres'

# Logging
LOG_PATH = 'log/log_1point3acres'
LOG_FILE = LOG_PATH + '/' + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + '.log'

# Cookies
COOKIES_FILE = 'cookies/acres.txt'

# MySQL
MYSQL_DB = '1point3acres'

# TABLE_INFO: pk, fk refer to primary key and foreign key, they must be iterable
TABLE_INFO = {
    'board': {
        'attrs': {
            'board_url': 'varchar(100)',
            'board_name': 'nvarchar(40)',
            'pages': 'int',
        },
        'pk': ('board_url',),
        'engine': 'MyISAM',
    },

    'post': {
        'attrs': {
            'post_url': 'varchar(100)',
            'post_name': 'nvarchar(100)',
            'board_url': 'nvarchar(100)',
            'board_name': 'nvarchar(40)',
            'user_url': 'varchar(100)',
            'user_name': 'nvarchar(30)',
            'replies': 'int',
            'pv': 'int',
            'date_time': 'datetime',
            'content': 'text',
            'context': 'text',
        },
        'pk': ('post_url',),
        'engine': 'MyISAM',
    },

    'user': {
        'attrs': {
            'user_url': 'varchar(100)',
            'uid': 'int',
            'user_name': 'nvarchar(30)',
            'profile': 'text',
        },
        'pk': ('user_url',),
        'engine': 'MyISAM',
    },
}
