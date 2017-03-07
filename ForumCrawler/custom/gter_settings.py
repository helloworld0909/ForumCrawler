# -*- coding: utf-8 -*-
import time
# Logging
LOG_PATH = 'gter_log'
LOG_FILE = LOG_PATH + '/' + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + '.log'

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