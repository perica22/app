class Verificator:
    """
   Base class for mock verification. Every component verification class should
   inherit this class.
   """
    def __init__(self, mocks=None, **kwargs):
        self.mocks = mocks
