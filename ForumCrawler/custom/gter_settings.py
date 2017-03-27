# -*- coding: utf-8 -*-
import time
# Logging
LOG_PATH = 'log/log_gter'
LOG_FILE = LOG_PATH + '/' + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + '.log'

# Cookies
COOKIES_FILE = 'cookies/gter.txt'

# MySQL
MYSQL_DB = 'gter'

# TABLE_INFO: pk, fk refer to primary key and foreign key, they must be iterable
TABLE_INFO = {
    'offer': {
        'attrs': {
            'uid': 'int',
            'school': 'varchar(100)',
            'degree': 'varchar(10)',
            'major': 'varchar(30)',
            'result': 'varchar(20)',
            'enroll_year': 'varchar(10)',
            'enroll_semester': 'varchar(10)',
            'notice_time': 'date'
        },
        'pk': ('uid',),
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
