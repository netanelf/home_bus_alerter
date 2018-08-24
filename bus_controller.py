from __init__ import *


class BusController(object):
    def __init__(self):
        self._root = tk.Tk()
        self._bus_view = BusView(master=self._root, controller=self)
        self._bus_data = HomeBusAlerter()
        self._is_running = False

    def run(self):
        self._is_running = True

        ts_thread = threading.Thread(target=self.update_time_thread)
        ts_thread.start()

        tt_thread = threading.Thread(target=self.update_time_tables_thread)
        tt_thread.start()
        self._root.mainloop()

    def update_time_thread(self):
        while self._is_running:
            ts = datetime.now().strftime(cfg.TIME_FORMAT)
            self._bus_view.update_time(ts=ts)
            time.sleep(1)

    def update_time_tables_thread(self):
        while self._is_running:
            d = self._bus_data.get_data_from_bus_station_num([cfg.STATIONS_LINES_DICTIONARY.keys()][0], [cfg.STATIONS_LINES_DICTIONARY.values()][0])
            self._bus_view.update_time_tables(data=d)


    def kill(self):
        self._is_running = False


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
    init_logging(logging.DEBUG)
    controller = BusController()
    controller.run()

