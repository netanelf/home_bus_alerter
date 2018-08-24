from __init__ import *


class BusView(tk.Frame):

    def __init__(self, master: tk.Tk, controller: 'BusController'):
        super(BusView, self).__init__(master=master)
        self._logger = logging.getLogger('{}.{}'.format(cfg.LOGGER_BASE_NAME, self.__class__.__name__))
        self._master = master
        self._controller = controller
        self._master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self._table_lines = 0
        self._build_gui()
        self._logger.info('finished init')

    def _build_gui(self):
        self.grid()
        self.master.title("Home bus alerter")
        self.master.geometry("{}x{}".format(*cfg.GUI_SIZE))
        self._one_line_time_guis = {}

        self.clock_var = tk.StringVar()
        self.clock_var.set('')
        self.clock_lbl = ttk.Label(self, textvariable=self.clock_var, font=(cfg.GUI_FONT, cfg.GUI_FONT_SIZE))
        self.clock_lbl.grid(row=self._table_lines, column=0, sticky='WN')
        self._table_lines += 1

        h = OneLineTimeGui.get_header(self)
        self.grid(row=self._table_lines, column=0, sticky='WN')
        self._table_lines += 1

        for station_num, buses in cfg.STATIONS_LINES_DICTIONARY.items():
            for b in buses:
                self._logger.debug('creating gui for station: {}, bus: {}'.format(station_num, b))
                o = OneLineTimeGui(master=self, station_num=station_num, bus_num=b)
                self.grid(row=self._table_lines, column=0, sticky='WN')
                self._one_line_time_guis[(station_num, b)] = o
                self._table_lines += 1

    def update_time(self, ts: str):
        self.clock_var.set(ts)

    def update_time_tables(self, data: List['LineData'], time_stamp: datetime):
        for d in data:
            line = d.line_num
            t = d.arrivel_time
            s = d.station_num
            dest = d.line_destination
            last_updated = int((datetime.now() - time_stamp).total_seconds())

            g = self._one_line_time_guis.get((s, line), None)
            if g is None:
                g = OneLineTimeGui(master=self, station_num=s, bus_num=line)
                self.grid(row=self._table_lines, column=0, sticky='WN')
                self._table_lines += 1
                self._one_line_time_guis[(s, line)] = g

            g.update_data(minutes_arivall=t, last_updated_sec=last_updated)

    def on_closing(self):
        self._controller.kill()
        self._master.destroy()
        self._logger.info('gui killed')


class OneLineTimeGui(ttk.Frame):
    # station, station num, bus, to?, minutes, last updated[sec]
    def __init__(self, master: any, station_num: any, bus_num: any):
        super(OneLineTimeGui, self).__init__(master=master)
        self._master = master
        self._station_num = station_num
        self._bus_num = bus_num
        self._build_gui()

    def _build_gui(self):
        self.grid(sticky='W', padx=50, pady=10)
        self.station_name_lbl = ttk.Label(self, text="Name", font=(cfg.GUI_FONT, cfg.GUI_FONT_SIZE))
        self.station_num_lbl = ttk.Label(self, text="{}".format(self._station_num), font=(cfg.GUI_FONT, cfg.GUI_FONT_SIZE))
        self.bus_num_lbl = ttk.Label(self, text=self._bus_num, font=(cfg.GUI_FONT, cfg.GUI_FONT_SIZE))

        self.station_name_lbl.grid(row=0, column=0, columnspan=1)
        self.station_num_lbl.grid(row=0, column=1, columnspan=1)
        self.bus_num_lbl.grid(row=0, column=2, columnspan=1)

        self.minutes_var = tk.IntVar()
        self.minutes_var.set('NA')
        self.minutes_lbl = ttk.Label(self, textvariable=self.minutes_var, font=(cfg.GUI_FONT, cfg.GUI_FONT_SIZE))
        self.minutes_lbl.grid(row=0, column=3, columnspan=1)

        self.last_updated_var = tk.IntVar()
        self.last_updated_var.set('NA')
        self.last_updated_lbl = ttk.Label(self, textvariable=self.minutes_var, font=(cfg.GUI_FONT, cfg.GUI_FONT_SIZE))
        self.last_updated_lbl.grid(row=0, column=4, columnspan=1)

    def update_data(self, minutes_arivall: any, last_updated_sec: any):
        self.minutes_var.set(minutes_arivall)
        self.last_updated_var.set(last_updated_sec)

    @staticmethod
    def get_header(master):
        header = OneLineTimeGui(master=master, station_num='Station Number', bus_num='Bus Number')
        header.update_data(minutes_arivall='Minutes to Arrival', last_updated_sec='Last Updated')
        return header