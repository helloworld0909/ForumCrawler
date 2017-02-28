import os
import re
import time
from ForumCrawler.settings import LOG_PATH


class LogErrorParser:

    def __init__(self):
        self.log_absolute_path = os.getcwd() + '/' + LOG_PATH
        self.log_list = [self.log_absolute_path + '/' + log_file for log_file in os.listdir(self.log_absolute_path)]

    def get_parse_error(self, filename=time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + '.txt'):
        output = open(filename, 'w')
        for log_path in self.log_list:
            with open(log_path, 'r') as log:
                for line in log:
                    # Format: <Category> url = <url>
                    search = re.search('(.*) url = (.*)', line)
                    if search:
                        output.write(search.group(1) + ' ' + search.group(2) + '\n')
        output.close()

    def get_other_error(self, filename):
        pass
