import logging
import os
import sys
sys.path.append(os.getcwd())
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from typing import List
#from pyvirtualdisplay import Display

#display = Display(visible=0, size=(480,320))
#display.start()

class LineData(object):
    def __init__(self, line_num: int, line_destination: str, arrivel_time: int):
        self.line_num = line_num
        self.line_destination = line_destination
        self.arrivel_time = arrivel_time

    def __repr__(self):
        return 'line: {}, destination: {}, arivel minutes: {}'.format(self.line_num, self.line_destination, self.arrivel_time)


class HomeBusAlerter(object):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._firefox_profile = webdriver.FirefoxProfile()
        self._firefox_profile.set_preference('permissions.default.image', 2)
        #self._firefox_options = Options()
        #self._firefox_options.set_headless(headless=True)
        self._driver = webdriver.Firefox(firefox_profile=self._firefox_profile)
        #self._driver = webdriver.PhantomJS()

    def get_data_from_bus_station_num(self, bus_station_num: int, line_filter=[]):
        self._logger.info('trying to get data on station no: {}'.format(bus_station_num))
        url = 'https://bus.gov.il/?language=en#/realtime/1/0/2/{}'.format(bus_station_num)
        if self._driver.current_url != url:
            self._driver.get(url)
        else:
            self._driver.refresh()
        self._wait_for_class(class_name='TableLines', timeout_s=20)
        time.sleep(1)  # additional

        data = self._parse_rendered_data()
        try:
            if len(data) > 0:
                if len(line_filter) > 0:
                    filtered_data = []
                    for d in data:
                        if d.line_num in line_filter:
                            filtered_data.append(d)
                    return filtered_data
                else:
                    return data
            else:  # data empty
                return data
        except Exception as ex:
            self._logger.exception(ex)

    def _wait_for_class(self, class_name: str, timeout_s: int):
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, class_name))
            WebDriverWait(self._driver, timeout_s).until(element_present)
        except TimeoutException:
            self._logger.error('{} did not load in {} seconds'.format(class_name, timeout_s))

    def _parse_rendered_data(self) -> List[LineData]:
        data = []
        try:
            a = self._driver.find_element_by_class_name('TableLines')
            b = a.text.split('\n')

            data_in_threes = [b[x:x+3] for x in range(0, len(b), 3)]
            for (n, d, a) in data_in_threes:
                line_num = int(n)
                line_dest = d
                if a == '↓ In station':
                    line_arival = 0
                else:
                    line_arival = int(a.split(' ')[0])

                l = LineData(line_num=line_num, line_destination=line_dest, arrivel_time=line_arival)
                data.append(l)

            self._logger.debug('found data: {}'.format(data))
        except ValueError as ex:
            self._logger.error(data_in_threes)
            self._logger.exception(ex)
        except Exception as ex:
            self._logger.exception(ex)

        return data


def init_logging(level):
    root_logger = logging.getLogger()
    root_logger.setLevel(level=level)
    #file_name = os.path.join('logs', 'BulboardServer_{}'.format(datetime.now().strftime('%d_%m_%y__%H_%M_%S')))
    #file_handler = DiskSpaceRotatingFileHandler(folder_max_size=10E6, filename=file_name, maxBytes=1E6, backupCount=10000)
    formatter = logging.Formatter(fmt=u'%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    #file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logging._defaultFormatter = logging.Formatter(u"%(message)s")  # so utf8 messages will not crash the logging
    #root_logger.addHandler(hdlr=file_handler)
    root_logger.addHandler(hdlr=console_handler)


if __name__ == '__main__':
    init_logging(logging.INFO)
    a = HomeBusAlerter()
    for i in range(5):
        d = a.get_data_from_bus_station_num(bus_station_num=43035, line_filter=[])
        logging.info(d)
        time.sleep(10)
    #display.stop()
