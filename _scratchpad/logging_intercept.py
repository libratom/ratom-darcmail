# https://stackoverflow.com/a/911944
# also see: https://realpython.com/python-metaclasses/#custom-metaclasses

import logging
logger = logging.getLogger(__name__)

class Foo():
    
    def __init__(self, name):
        self.name = name

    def bar(self, n):
        return n + 1

    def __getattribute__(self, name):
        """ Soem doc """
        global logger

        def make_interceptor(callble):
            def func(*args, **kwargs):
                logger.warning("{} {}".format(args, kwargs))
                return callble(*args, **kwargs)
            return func

        try:
            att = object.__getattribute__(self, name)
            print(dir(att))
        except Exception as err:
            logger.error(err)
            return#raise err

        if callable(att):
            return make_interceptor(att)
        else:
            logger.warning(False)
            return att

f = Foo("Nitin")
