class ProviderNotSupportedException(Exception):

    def __init__(self, provider: str):
        self.provider = provider