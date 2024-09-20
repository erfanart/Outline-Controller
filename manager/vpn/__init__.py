from .server import Server
from .keys import Keys
from manager.db import VpnDb
from manager.setting import *

def update():
    vpndb = VpnDb().AppDB
    server = Server(CONFIG['servers']['url'],CONFIG['servers']['pass'])
    vpn = Keys(server)

    vpndb.make_db()
    for k in vpn.all:
        vpn.info("key_id",k.key_id)

        key = {}

        for a in vpn.attrs:
                key[a]= f"{getattr(vpn, a)}"

        vpndb.db.add_record("keys",key,{"key_id" : key["key_id"]})
        vpndb.info("key_id","keys",key["key_id"])

        for a in  vpn.attrs:
            vpndb.db.update(table="keys",condition={"key_id": k.key_id }, data={a:f"{getattr(vpn, a)}"})

        if not vpn.check_exist(key):
            vpndb.db.delete_record("keys",f'key_id = {key["key_id"]}' )
        else:
            status = vpn.check_date(vpndb.info(mode="key_id",table="keys",value=key["key_id"]))
            if status == "active" :
                key["status"] = vpn.check_usage(key)

            elif status == "expired":
                key["status"] = status

            else:
                vpn.extend_expire(key=key)
        vpndb.update(table="keys",key=key)