from __init__ import *


class LineData(object):
    def __init__(self, line_num: int, line_destination: str, arrivel_time: int, station_num: int, creation_time: datetime, station_name: str=''):
        self.station_num = station_num
        self.station_name = station_name
        self.line_num = line_num
        self.line_destination = line_destination
        self.arrival_time = arrivel_time
        self.creation_time = creation_time

    def __repr__(self):
        return 'station: {}, line: {}, destination: {}, arrival minutes: {}, creatin_time: {}'\
            .format(
                self.station_num, self.line_num, self.line_destination, self.arrival_time, self.creation_time
            )


class HomeBusAlerter(object):
    def __init__(self):
        self._logger = logging.getLogger('{}.{}'.format(cfg.LOGGER_BASE_NAME, self.__class__.__name__))
        self._firefox_profile = webdriver.FirefoxProfile()
        self._firefox_profile.set_preference('permissions.default.image', 2)
        #self._firefox_options = Options()
        #self._firefox_options.set_headless(headless=True)
        self._driver = webdriver.Firefox(firefox_profile=self._firefox_profile)
        #self._driver = webdriver.PhantomJS()
        self._unsuccessful_reads_counter = 0

    def get_data_from_bus_station_num(self, bus_station_num: int, line_filter=[], bus_station_name: int='') -> List[LineData]:
        self._logger.info('trying to get data on station no: {}'.format(bus_station_num))
        url = 'https://bus.gov.il/?language=en#/realtime/1/0/2/{}'.format(bus_station_num)
        if self._unsuccessful_reads_counter > cfg.MAX_UNSUCCESSFUL_READS__CONS:
            self._restart_driver()

        try:
            if self._driver.current_url != url:
                self._driver.get(url)
            else:
                self._driver.refresh()
            self._wait_for_class(class_name='TableLines', timeout_s=20)
        except Exception as ex: # have seen times that refresh/ wait finished with an exception
            self._logger.exception(ex)
            self._unsuccessful_reads_counter += 1
            return []

        time.sleep(1)  # additional

        data = self._parse_rendered_data(station_num=bus_station_num, station_name=bus_station_name)
        try:
            if len(data) > 0:
                self._unsuccessful_reads_counter = 0
                if len(line_filter) > 0:
                    filtered_data = []
                    for d in data:
                        if d.line_num in line_filter:
                            filtered_data.append(d)
                    return filtered_data
                else:
                    return data
            else:  # data empty
                self._unsuccessful_reads_counter += 1
                return data
        except Exception as ex:
            self._logger.exception(ex)
            self._unsuccessful_reads_counter += 1

    def _wait_for_class(self, class_name: str, timeout_s: int):
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, class_name))
            WebDriverWait(self._driver, timeout_s).until(element_present)
        except TimeoutException:
            self._logger.error('{} did not load in {} seconds'.format(class_name, timeout_s))

    def _parse_rendered_data(self, station_num: int, station_name: str='') -> List[LineData]:
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

                l = LineData(station_num=station_num, line_num=line_num, line_destination=line_dest, arrivel_time=line_arival, creation_time=datetime.now(), station_name=station_name)
                data.append(l)

            self._logger.debug('found data: {}'.format(data))
        except ValueError as ex:
            self._logger.error(data_in_threes)
            self._logger.exception(ex)
        except Exception as ex:
            self._logger.exception(ex)

        return data

    def kill(self):
        self._driver.quit()
        self._logger.info('webdriver killed')

    def _restart_driver(self):
        self._logger.warning('restarting driver, unsuccessful_reads_counter: {}'.format(self._unsuccessful_reads_counter))
        self._driver.quit()
        time.sleep(5)
        self._driver = webdriver.Firefox(firefox_profile=self._firefox_profile)
        self._logger.warning('new driver loaded')



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
