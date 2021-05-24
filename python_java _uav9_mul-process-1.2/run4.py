import run


class Run(run.Run):

    def __init__(self, id):
        self.connection_string = '127.0.0.1:14581'
        self.id = id