# coding=utf-8
from __future__ import absolute_import
import Adafruit_CharLCD as LCD
import octoprint.plugin

class PiprintPlugin(octoprint.plugin.StartupPlugin,
                    octoprint.plugin.ProgressPlugin,
                    octoprint.plugin.ShutdownPlugin,
                    octoprint.plugin.EventHandlerPlugin):

    def on_after_startup(self):
        """
        Runs when plugin is started. Turn on and clear the LCD.
        """
        self._logger.info("PiPrint starting")
        lcd = LCD.Adafruit_CharLCDPlate()
        lcd.clear()

    def on_event(self, event, payload):
        """
        Called when an event occurs. Displays print updates; turns off LCD when print stops for any reason.
        :param event: Event which just happened.
        :param payload: Dictionary of data passed with the event
        """
        # Only handle print events
        if 'Print' in event:
            useful_print_events = ['Resumed', 'Started']
            if any(e in event for e in useful_print_events):
                self.__class__._write_to_lcd(str(event))
            else:
                self.__class__._write_to_lcd("")
                self.__class__._turn_lcd_off()

    def on_print_progress(self, storage, path, progress):
        """
        Called on 1% print progress updates. Displays the new progress on the LCD.
        :param storage: File being printed
        :param path: Path of file being printed
        :param progress: Progress of print
        """
        if not self._printer.is_printing():
            return
        self.__class__._write_to_lcd("Printing\n%s" % self.__class__._format_progress_bar(progress))

    def on_shutdown(self):
        """
        Called on shutdown of OctoPrint. Turn off the LCD.
        """
        self._logger.info("PiPrint turning off LCD")
        self.__class__._turn_lcd_off()

    # Class methods (assisting functions)
    @classmethod
    def _format_progress_bar(cls, progress):
        """
        Create a formatted string 'progress bar' based on the given value
        :param progress: Progress (0-100) of the print
        :return: Formatted string representing a progress bar
        """
        filler = "#" * int(round(progress / 10))
        spaces = " " * (10 - len(filler))
        return "[{}{}] {}%".format(filler, spaces, str(progress))

    @classmethod
    def _turn_lcd_off(cls):
        """
        Turn the LCD off by setting the backlight to zero.
        """
        lcd = LCD.Adafruit_CharLCDPlate()
        lcd.set_backlight(0)

    @classmethod
    def _turn_lcd_on(cls):
        """
        Turn the LCD on by setting the backlight to one.
        """
        lcd = LCD.Adafruit_CharLCDPlate()
        lcd.set_backlight(1.0)

    @classmethod
    def _write_to_lcd(cls, message):
        """
        Write a string message to the LCD. Displays the text on the LCD display.
        :param message: Message to display on the LCD
        """
        cls._turn_lcd_on()
        lcd = LCD.Adafruit_CharLCDPlate()
        lcd.message(message)

__plugin_name__ = "PiPrint Plugin"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = PiprintPlugin()