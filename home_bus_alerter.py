import logging
from requests_html import HTMLSession, HTML


class HomeBusAlerter(object):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._session = HTMLSession()

    def get_data_from_bus_station_num(self, bus_station_num: int):
        self._logger.info('trying to get data on station no: {}'.format(bus_station_num))
        r = self._session.get('https://mslworld.egged.co.il/?language=en#/realtime/1/0/2/{}'.format(bus_station_num))
        r.html.render()
        self._parse_egged_rendered_data(rendered_html=r.html)

    def _parse_egged_rendered_data(self, rendered_html: HTML):
        try:
            a = rendered_html.find('.TableLines')
            b = a[0].text.split('tr')
            c = b[0].split('\n')

            data = []
            data_in_threes = [c[x:x+3] for x in range(0, len(c), 3)]
            for (n, d, a) in data_in_threes:
                line_num = int(n)
                line_dest = d
                line_arival = int(a.split(' ')[0])

                l = LineData(line_num=line_num, line_destination=line_dest, arrivel_time=line_arival)
                data.append(l)

            self._logger.info('found data: {}'.format(data))
        except ValueError as ex:
            self._logger.error(data_in_threes)
            self._logger.exception(ex)

        return data


class LineData(object):
    def __init__(self, line_num: int, line_destination: str, arrivel_time: int):
        self.line_num = line_num
        self.line_destination = line_destination
        self.arrivel_time = arrivel_time

    def __repr__(self):
        return 'line: {}, destination: {}, arivel minutes: {}'.format(self.line_num, self.line_destination, self.arrivel_time)


def init_logging():
    logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    init_logging()
    a = HomeBusAlerter()
    a.get_data_from_bus_station_num(bus_station_num=2180)

