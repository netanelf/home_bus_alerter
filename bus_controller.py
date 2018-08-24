from __init__ import *


class BusController(object):
    def __init__(self):
        self._logger = logging.getLogger('{}.{}'.format(cfg.LOGGER_BASE_NAME, self.__class__.__name__))
        self._root = tk.Tk()
        self._bus_view = BusView(master=self._root, controller=self)
        self._bus_data = HomeBusAlerter()
        self._is_running = False
        self._logger.info('finished init')

    def run(self):
        self._is_running = True

        self.ts_thread = threading.Thread(target=self.update_time_thread)
        self.ts_thread.start()

        self.tt_thread = threading.Thread(target=self.update_time_tables_thread)
        self.tt_thread.start()
        self._root.mainloop()
        self._logger.info('main loop done')

    def update_time_thread(self):
        while self._is_running:
            ts = datetime.now().strftime(cfg.TIME_FORMAT)
            self._bus_view.update_time(ts=ts)
            time.sleep(1)

    def update_time_tables_thread(self):
        while self._is_running:
            for station_num, line_filter in cfg.STATIONS_LINES_DICTIONARY.items():
                request_ts = datetime.now()
                d = self._bus_data.get_data_from_bus_station_num(bus_station_num=station_num, line_filter=line_filter)
                self._bus_view.update_time_tables(data=d, time_stamp=request_ts)
            time.sleep(1)

    def kill(self):
        self._is_running = False
        self._bus_data.kill()
        self.ts_thread.join(5)
        self.tt_thread.join(5)
        self._logger.info('all threads killed')


def init_logging(level):
    root_logger = logging.getLogger()
    root_logger.setLevel(level=logging.INFO)
    #file_name = os.path.join('logs', 'BulboardServer_{}'.format(datetime.now().strftime('%d_%m_%y__%H_%M_%S')))
    #file_handler = DiskSpaceRotatingFileHandler(folder_max_size=10E6, filename=file_name, maxBytes=1E6, backupCount=10000)
    formatter = logging.Formatter(fmt=u'%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    #file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logging._defaultFormatter = logging.Formatter(u"%(message)s")  # so utf8 messages will not crash the logging
    #root_logger.addHandler(hdlr=file_handler)
    root_logger.addHandler(hdlr=console_handler)

    mylogger = logging.getLogger(cfg.LOGGER_BASE_NAME)
    mylogger.setLevel(level=level)


if __name__ == '__main__':
    init_logging(logging.DEBUG)
    controller = BusController()
    controller.run()

