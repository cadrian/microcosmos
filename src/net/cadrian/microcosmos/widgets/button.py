from pysge.objects.widgets import NiceButton
from pysge.utils.data import DataContainer


class TemplateButton:
    def __init__(self, config):
	self._config = config
	self.standAlone = False

    def getButton(self, customize=None):
	config = dict(self._config._symbols)
	if customize is not None:
	    customize(config)
	return NiceButton(DataContainer(**config))
