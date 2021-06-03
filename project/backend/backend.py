import http.server
import socketserver
import json
import os
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        self.data_string=self.rfile.read(int(self.headers['Content-Length']))
        user_input=json.loads(self.data_string)
        with open("backend/user_input.json","w") as outfile:
            json.dump(user_input,outfile)
        os.system("python3 model_Markowitz/marko.py")      
        self.send_response(200)
        self.end_headers()
        feedback={}
        with open('output/range.json') as json_file:
            feedback["max_mini"]=json.load(json_file)
        with open('output/frontier.json') as json_file:
            feedback["frontier"]=json.load(json_file)
        with open('output/allocation.json') as json_file:
            feedback["allocation"]=json.load(json_file)
        self.wfile.write(json.dumps(feedback).encode("utf8"))
        

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()
        return

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        # self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Headers','Content-Type');
        # self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super(MyHandler, self).end_headers()
        

handler_object=MyHandler

PORT=8000
my_server=socketserver.TCPServer(("",PORT),handler_object)

try:
    my_server.serve_forever()
except KeyboardInterrupt:
    pass

my_server.server_close()