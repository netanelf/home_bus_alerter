import logging
import os
import datetime
from requests_html import HTMLSession, HTML
import time
from typing import List


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
        #self._session = None

    def get_data_from_bus_station_num(self, bus_station_num: int, line_filter=[]):
        self._logger.info('trying to get data on station no: {}'.format(bus_station_num))
        s = HTMLSession()
        r = s.get('https://mslworld.egged.co.il/?language=en#/realtime/1/0/2/{}'.format(bus_station_num))
        r.html.render()
        data = self._parse_egged_rendered_data(rendered_html=r.html)
        s.close()
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
            else: # data empty
                return data
        except Exception as ex:
            self._logger.exception(ex)


    def _parse_egged_rendered_data(self, rendered_html: HTML) -> List[LineData]:
        data = []
        try:
            a = rendered_html.find('.TableLines')
            b = a[0].text.split('tr')
            c = b[0].split('\n')

            data_in_threes = [c[x:x+3] for x in range(0, len(c), 3)]
            for (n, d, a) in data_in_threes:
                line_num = int(n)
                line_dest = d
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
    while(True):
        d = a.get_data_from_bus_station_num(bus_station_num=2180, line_filter=[12])
        logging.info(d)
        time.sleep(10)
