import os
import sys
import time
import json
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler

open_addr={}
last_time=time.time()
class MyRequestHandler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.0"
    server_version = "PSHS/0.1"
    sys_version = "Python/3.7.x"

    def do_GET(self):
        if self.path == "/rwj":
            addr=self.client_address[0]
            if addr not in open_addr:
                print("add sucessfully:{}".format(addr))
                add = "firewall-cmd --permanent --add-rich-rule=\"rule family=\"ipv4\" source address=\"{}\" port protocol=\"tcp\" port=\"12001\" accept\"".format(addr)
                os.system(add)
                os.system("firewall-cmd --reload")
                open_addr[addr[0]] = time.time()
            else:
                pass
            process = 0
            for item in open_addr:
                if time.time()-open_addr[item]>3600*10:
                    remove = "firewall-cmd --permanent --add-rich-rule=\"rule family=\"ipv4\" source address=\"{}\" port protocol=\"tcp\" port=\"12001\" accept\"".format(item)
                    os.system(remove)
                    process += 1
            if process>0:
                os.system("firewall-cmd --reload")
            req = {"success": "true"}
            self.send_response(200)
            self.send_header("Content-type", "json")
            self.end_headers()
            rspstr = json.dumps(req)
            self.wfile.write(rspstr.encode("utf-8"))

        else:
            pass

    def do_POST(self):
        if self.path == "/signin":
            print("postmsg recv, path right")
        else:
            print("postmsg recv, path error")
            data = self.rfile.read(int(self.headers["content-length"]))
            data = json.loads(data)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            rspstr = "recv ok, data = "
            rspstr += json.dumps(data, ensure_ascii=False)
            self.wfile.write(rspstr.encode("utf-8"))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        # set the target where to mkdir, and default "D:/web"
        MyRequestHandler.target = sys.argv[1]
    try:
        server = HTTPServer(("", 8081), MyRequestHandler)
        print("pythonic-simple-http-server started, serving at http://localhost:8080")
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()

