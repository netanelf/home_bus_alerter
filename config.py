

GUI_SIZE = (480, 320)
GUI_FONT_SIZE = 12
GUI_FONT = "Arial"
TIME_FORMAT = '%H:%M:%S'
TIME_WAIT_BETWEEN_REFRESH_SEC = 10
MAX_UNSUCCESSFUL_READS__CONS = 10  # if we do not manage to get data this times in a row - try to fix something

LOGGER_BASE_NAME = 'bus'

STATIONS_LINES_DICTIONARY = \
    {
        2180: {'name': 'Pat\nYehuda\nHaNassi', 'filter': (12,)},
        2181: {'name': 'Pat\nYehuda\nHanassi2', 'filter': (22,)}
    }
