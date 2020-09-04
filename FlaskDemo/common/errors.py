# coding=utf-8
import logging


class ShowError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


if __name__ == '__main__':
    try:
        raise ShowError(u'我的')
    except ShowError as e:
        logging.warn(e.message)
