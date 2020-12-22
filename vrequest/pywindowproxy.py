# -*- coding:UTF-8 -*-
import ctypes
import winreg
class WindowProxySetting:
    def __init__(self, proxy="127.0.0.1:8888"):
        proxy_path = r'Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings'
        self.proxy = proxy
        self.root = winreg.HKEY_CURRENT_USER
        self.hKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, proxy_path)
        self.set_proxy = [
            [proxy_path, "ProxyEnable", winreg.REG_DWORD, 1],
            [proxy_path, "ProxyServer", winreg.REG_SZ, self.proxy],
        ]
    def _flash(self):
        # 让修改立即生效
        try:
            internet_set_option = ctypes.windll.Wininet.InternetSetOptionW    
            internet_set_option(0, 39, 0, 0)
            internet_set_option(0, 37, 0, 0)
        except:pass
    def open(self):
        self.set_proxy[0][3] = 1
        for keypath, value_name, value_type, value in self.set_proxy:
            self.hKey = winreg.CreateKey(self.root, keypath)
            winreg.SetValueEx(self.hKey, value_name, 0, value_type, value)
        self._flash()
    def close(self):
        self.set_proxy[0][3] = 0
        for keypath, value_name, value_type, value in self.set_proxy:
            self.hKey = winreg.CreateKey(self.root, keypath)
            winreg.SetValueEx(self.hKey, value_name, 0, value_type, value)
        self._flash()
    def get_state(self):
        value, type = winreg.QueryValueEx(self.hKey, "ProxyEnable")
        return bool(value)
    def get_server(self):
        value, type = winreg.QueryValueEx(self.hKey, "ProxyServer")
        return value

if __name__ == '__main__':
    wproxy = WindowProxySetting()
    v = wproxy.get_state()
    print(v)
    v = wproxy.get_server()
    print(v)

    # wproxy.open()
    # wproxy.close()