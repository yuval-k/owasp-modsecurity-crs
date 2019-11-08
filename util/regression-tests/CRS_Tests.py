from ftw import ruleset, logchecker, testrunner
import datetime
import pytest
import sys
import re
import os


def test_crs(ruleset, test, logchecker_obj):
    runner = testrunner.TestRunner()
    for stage in test.stages:
        runner.run_stage(stage, logchecker_obj)


class FooLogChecker(logchecker.LogChecker):
    def __init__(self, config):
        super(FooLogChecker, self).__init__()
        self.log_location = config['log_location_linux']
        self.log_date_regex = config['log_date_regex']
        self.log_date_format = config['log_date_format']

    def reverse_readline(self, filename):
        with open(filename) as f:
            f.seek(0, os.SEEK_END)
            position = f.tell()
            line = ''
            while position >= 0:
                f.seek(position)
                next_char = f.read(1)
                if next_char == "\n":
                    yield line[::-1]
                    line = ''
                else:
                    line += next_char
                position -= 1
            yield line[::-1]

    def get_logs(self):
        pattern = re.compile(r'%s' % self.log_date_regex)
        our_logs = []
        matched = False
        for lline in self.reverse_readline(self.log_location):
            # Extract dates from each line
            match = re.match(pattern, lline)
            if match or matched:
                if not match:
                    # regex didn't match - the line doesnt start with a date.
                    # this can happend if a log line contains newlines. As we are in the correct date range.
                    # append it as well
                    our_logs.append(lline)
                    continue

                log_date = match.group(1)
                log_date = datetime.datetime.strptime(
                    log_date, self.log_date_format)
                # hack: envoy logs in the container in UTC, so convert log_date to localtime
                # EST = UTC-5
                DELTA_TIME = -5
                log_date = log_date.replace(hour = log_date.hour + DELTA_TIME)
                # NGINX doesn't give us microsecond level by detail, round down.
                if "%f" not in self.log_date_format:
                    ftw_start = self.start.replace(microsecond=0)
                else:
                    ftw_start = self.start
                ftw_end = self.end
                if log_date <= ftw_end and log_date >= ftw_start:
                    matched = True
                    our_logs.append(lline)
                # If our log is from before FTW started stop
                if log_date < ftw_start:
                    break
        return our_logs


@pytest.fixture(scope='session')
def logchecker_obj(config):
    return FooLogChecker(config)
