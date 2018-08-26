import logging
from datetime import datetime
import time
import threading

import tkinter as tk
import tkinter.ttk as ttk

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from typing import TYPE_CHECKING, List, Dict, Tuple
from typing import List

import config as cfg
from bus_gui import BusView
from home_bus_alerter import HomeBusAlerter
from bus_controller import BusController
from home_bus_alerter import LineData


#from pyvirtualdisplay import Display

#display = Display(visible=0, size=(480,320))
#display.start()