# -*- coding: utf-8 -*-
import time

JOBDIR = 'job_gter'

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
            'url': 'varchar(500)',
            'offer_type': 'varchar(100)',
            'uid': 'int',

            'school': 'varchar(500)',
            'degree': 'varchar(500)',
            'major': 'varchar(500)',
            'result': 'varchar(500)',
            'enroll_year': 'varchar(500)',
            'enroll_semester': 'varchar(500)',
            'notice_time': 'date',

            'toefl': 'varchar(500)',
            'ielts': 'varchar(500)',
            'gre': 'varchar(500)',
            'sub': 'varchar(500)',
            'gmat': 'varchar(500)',
            'undergraduate_gpa': 'varchar(500)',
            'undergraduate_school': 'varchar(500)',
            'undergraduate_major': 'varchar(500)',
            'master_gpa': 'varchar(500)',
            'master_school':'varchar(500)',
            'master_major':'varchar(500)',
            'other_info': 'varchar(1000)',
        },
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
