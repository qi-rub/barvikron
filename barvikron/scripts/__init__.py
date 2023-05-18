import logging
import click


def enable_logging():
    logging.basicConfig(format="%(asctime)-25s %(message)s", level=logging.INFO)


class WeightParamType(click.ParamType):
    name = "weight"

    def convert(self, value, param, ctx):
        value = eval(value)
        if not isinstance(value, (tuple, list)):
            self.fail("%s is not a valid weight" % value, param, ctx)
        return value
