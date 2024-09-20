from outline_vpn.outline_vpn import OutlineVPN

class Server(OutlineVPN):  
    def __init__(self,url,cert) -> None:
        super().__init__(api_url=url,cert_sha256 = cert) 
        pass 
    