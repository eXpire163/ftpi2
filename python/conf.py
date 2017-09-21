"""This module does config blah."""

class Config(object):
    """ Config class to store the settings """

    # Global settings
    debug = True

    # MQTT Settings
    mqtt_server = "localhost"
    mqtt_port = 1833

    # MQTT Channels

    mqtt_channel = "ftpi2"

    @staticmethod
    def printme(source, msg, debug=True):
        """ prints the logs formatted """
        if bool(False):
            print "[INFO ] {}:\t{}".format(source, msg)

        elif Config.debug & debug:
            print "[DEBUG] {}:\t{}".format(source, msg)


    @staticmethod
    def show_config():
        """ show mqtt config """
        Config.printme("Config", "{} {}".format(Config.mqtt_server, Config.mqtt_port))
