from __init__ import *


class BusView(tk.Frame):

    def __init__(self, master: tk.Tk, controller: 'BusController'):
        super(BusView, self).__init__(master=master)
        self._logger = logging.getLogger('{}.{}'.format(cfg.LOGGER_BASE_NAME, self.__class__.__name__))
        self._master = master
        self._controller = controller
        self._master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self._table_lines = 0
        self._one_line_time_guis: Dict[Tuple[int, int], OneLineTimeGui] = {}
        self._build_gui()
        self._logger.info('finished init')

    def _build_gui(self):
        self.grid()
        self.master.title("Home bus alerter")
        self.master.geometry("{}x{}".format(*cfg.GUI_SIZE))

        self.clock_var = tk.StringVar()
        self.clock_var.set('')
        self.clock_lbl = ttk.Label(self, textvariable=self.clock_var, font=(cfg.GUI_FONT, cfg.GUI_FONT_SIZE))
        self.clock_lbl.grid(row=self._table_lines, column=0, sticky='WN')
        self._table_lines += 1

        self._header = OneLineTimeGui.get_header(self)
        self.grid(row=self._table_lines, column=0, sticky='WN')
        self._table_lines += 1

        for station_num, data in cfg.STATIONS_LINES_DICTIONARY.items():
            for b in data['filter']:
                self._logger.debug('creating gui for station: {}, bus: {}'.format(station_num, b))
                o = OneLineTimeGui(master=self, station_num=station_num, bus_num=b, station_name=data['name'])
                self.grid(row=self._table_lines, column=0, sticky='WN')
                self._one_line_time_guis[(station_num, b)] = o
                self._table_lines += 1

    def update_time(self, ts: str):
        self.clock_var.set(ts)

    def update_last_updated_time(self, station_num: int, bus_num: int, new_last_updated_time_sec: [int, str]):
        self._one_line_time_guis[(station_num, bus_num)].update_last_updated(new_last_updated=new_last_updated_time_sec)

    def update_time_tables(self, data: List['LineData']):
        for d in data:
            line = d.line_num
            t = d.arrival_time
            s = d.station_num
            dest = d.line_destination
            station_name = d.station_name
            last_updated = int((datetime.now() - d.creation_time).total_seconds())

            g = self._one_line_time_guis.get((s, line), None)
            if g is None:
                g = OneLineTimeGui(master=self, station_num=s, bus_num=line, station_name=station_name)
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
    def __init__(self, master: any, station_num: any, bus_num: any, station_name: str=''):
        super(OneLineTimeGui, self).__init__(master=master)
        self._master = master
        self._root = self.winfo_toplevel()
        self._station_num = station_num
        self._bus_num = bus_num
        self._station_name = station_name
        self._padx = 10
        self._pady = 10
        self._build_gui()

    def _build_gui(self):
        self.grid(sticky='N,E,W')
        self.station_name_lbl = ttk.Label(self, text=self._station_name, font=(cfg.GUI_FONT, cfg.GUI_FONT_SIZE))
        self.station_num_lbl = ttk.Label(self, text="{}".format(self._station_num), font=(cfg.GUI_FONT, cfg.GUI_FONT_SIZE))
        self.bus_num_lbl = ttk.Label(self, text=self._bus_num, font=(cfg.GUI_FONT, cfg.GUI_FONT_SIZE))

        self.station_name_lbl.grid(row=0, column=0, columnspan=1, padx=self._padx, pady=self._pady)
        self.station_num_lbl.grid(row=0, column=1, columnspan=1, padx=self._padx, pady=self._pady)
        self.bus_num_lbl.grid(row=0, column=2, columnspan=1, padx=self._padx, pady=self._pady)

        self.minutes_var = tk.IntVar()
        self.minutes_var.set('NA')
        self.minutes_lbl = ttk.Label(self, textvariable=self.minutes_var, font=(cfg.GUI_FONT, cfg.GUI_FONT_SIZE))
        self.minutes_lbl.grid(row=0, column=3, columnspan=1, padx=self._padx, pady=self._pady)

        self.last_updated_var = tk.IntVar()
        self.last_updated_var.set('NA')
        self.last_updated_lbl = ttk.Label(self, textvariable=self.last_updated_var, font=(cfg.GUI_FONT, cfg.GUI_FONT_SIZE))
        self.last_updated_lbl.grid(row=0, column=4, columnspan=1, padx=self._padx, pady=self._pady)

        for i in range(5):
            self.grid_columnconfigure(i, weight=3)

    def update_data(self, minutes_arivall: any, last_updated_sec: any):
        self.minutes_var.set(minutes_arivall)
        self.last_updated_var.set(last_updated_sec)

    def update_last_updated(self, new_last_updated: int):
        self.last_updated_var.set(new_last_updated)

    @staticmethod
    def get_header(master):
        header = OneLineTimeGui(master=master, station_num='Station\nnumber', bus_num='Bus\nnumber', station_name='Station\nname')
        header.update_data(minutes_arivall='Minutes\nto Arrival', last_updated_sec='Last\nUpdated [S]')
        return header