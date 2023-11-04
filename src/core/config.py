import configparser

# config_path = path.abspath(path.join(path.dirname(__file__), 'config.ini'))
import os

config_path = os.path.expanduser("~/Desktop/config.ini")
cf = configparser.ConfigParser()
cf.read(config_path, encoding='utf-8')

WINDOW_MAP = {1: [951, 410],
              2: [945, 480],
              3: [942, 555],
              4: [944, 627],
              5: [950, 698],
              6: [944, 773]
              }
REWARDS_MAP = {1: [[1491, 733]],
               2: [[1333, 733], [1620, 732]],
               3: [[1263, 726], [1477, 726], [1676, 732]],
               4: [[1161, 727], [1367, 728], [1576, 729], [1786, 729]]
               }
CHALLENGE_POINT_MAP = {
    '1': [1715, 553],
    '2': [1735, 625],
    '3': [1724, 701],
    '4': [1728, 767],
    '5': [1730, 843]
}


def save_config(session, key, value):
    cf.set(session, key, value)
    with open(config_path, 'w', encoding='utf-8') as configfile:
        cf.write(configfile)


def get(session, key):
    return cf.get(session, key)
