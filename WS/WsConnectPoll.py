class WsConnectPoll:
    def __init__(self) -> None:
        self._poll = dict()

    def add(self, ipport, obj):
        self._poll[ipport] = obj
        

    def get(self, ipport):
        return self._poll[ipport]

    def is_set(self, ipport):
        return ipport in self._poll.keys()