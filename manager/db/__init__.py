from manager.setting import CONFIG
from .sqllite import vpndb
class VpnDb:
    def __init__(self):
        self.type = CONFIG["database"]["type"]
        self.AppDB = self.dispatch()

    def dispatch(self):
        if self.type == "sqllite":
            return vpndb.VpnDb(CONFIG["database"]["path"])
        elif self.type == "mysql":
            pass