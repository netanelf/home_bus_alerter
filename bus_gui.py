from __init__ import *


class BusView(tk.Frame):

    def __init__(self, master: tk.Tk, controller: 'BusController'):
        #tk.Frame.__init__(self, master)
        super(BusView, self).__init__(master=master)
        self._logger = logging.getLogger(__name__)
        self._master = master
        self._controller = controller
        self._build_gui()

    def _build_gui(self):
        self.grid()
        self.master.title("Home bus alerter")
        self.master.geometry("{}x{}".format(*cfg.GUI_SIZE))
        self._one_line_time_guis = {}

        line = 0
        self.clock_var = tk.StringVar()
        self.clock_var.set('')
        self.clock_lbl = ttk.Label(self, textvariable=self.clock_var, font=(cfg.GUI_FONT, cfg.GUI_FONT_SIZE))
        self.clock_lbl.grid(row=line, column=0, sticky='WN')
        line += 1
        for station_num, buses in cfg.STATIONS_LINES_DICTIONARY.items():
            for b in buses:
                self._logger.debug('creating gui for station: {}, bus: {}'.format(station_num, b))
                o = OneLineTimeGui(master=self, station_num=station_num, bus_num=b)
                self.grid(row=line, column=0, sticky='WN')
                self._one_line_time_guis[(station_num, b)] = o
                line += 1

    def update_time(self, ts: str):
        self.clock_var.set(ts)

    def update_time_tables(self, data: List['LineData']):
        for d in data:
            line = d.line_num
            t = d.arrivel_time
            s = d.station_num
            dest = d.line_destination

            g = self._one_line_time_guis.get((s, line), None)
            if g is None:
                g = OneLineTimeGui(master=self, station_num=s, bus_num=line)
                self._one_line_time_guis[(s, line)] = g

            g.update_data(minutes_arivel=t)


class OneLineTimeGui(ttk.Frame):
    # station, station num, bus, to?, minutes, last updated[sec]
    def __init__(self, master: any, station_num: int, bus_num: int):
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
        self.minutes_var.set(-999)
        self.minutes_lbl = ttk.Label(self, textvariable=self.minutes_var, font=(cfg.GUI_FONT, cfg.GUI_FONT_SIZE))

    def update_data(self, minutes_arivel: int):
        self.minutes_var.set(minutes_arivel)