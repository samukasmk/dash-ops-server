import logging

logger = logging.getLogger(__name__)


class NodeEnvIsNone(Exception):
    def __init__(self, msg=None):
        Exception.__init__(self, msg)


class DomainEnvIsNone(Exception):
    def __init__(self, msg=None):
        Exception.__init__(self, msg)
