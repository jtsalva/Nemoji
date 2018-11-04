import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado import template
import json
import os
from string import Template
import wave
import time
import glob
import re
import json
import tornado
from db import new_log
from db import get_logs
from transcribe import transcribe
from sentiment import analyze_sentiment

HOSTNAME = 'htm.jtsalva.space'

current = {
    'caller': None,
    'transcription': None,
    'datetime': None
}

def convert():
    t = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    current['datetime'] = t
    f = wave.open('static/{}.wav'.format(t), 'wb')
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(16000)
    with open('static/audio.raw', 'rb') as src:
        f.writeframes(src.read())
    f.close()

def timestamps(d):
    p = d[0]
    output = [] 
    for ts in d:
        td = ts-p
        output.append(td*1000)
        p=ts
    with open('static/timestamps.json', "w") as f:
        f.write(json.dumps(output))


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        logs = get_logs()

        with open('static/index.html') as f:
            file = f.read()

        t = template.Template(file)

        self.content_type = 'text/html'
        self.write(t.generate(logs=logs))
        self.finish()

		
class CallHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        data={}
        data['hostname'] = HOSTNAME
        filein = open('ncco.json')
        src = Template(filein.read())
        filein.close()
        ncco = json.loads(src.substitute(data))
        self.write(json.dumps(ncco))
        self.set_header("Content-Type", 'application/json; charset="utf-8"')
        self.finish()


class EventHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        print(str(self.request.body))
        current['caller'] = json.loads(self.request.body.decode('utf-8'))['from']
        self.content_type = 'text/plain'
        self.write('ok')
        self.finish()
			

class WSHandler(tornado.websocket.WebSocketHandler):
    buffer = b''
    ts = []
    def check_origin(self, origin):
        return True
    def open(self):
        print("Websocket Call Connected")
    def on_message(self, message):
        self.ts.append(time.time())
        if type(message) != str:
            self.buffer += message
        else:
            print(message)
    def on_close(self):
        print("Websocket Call Disconnected")
        with open('static/audio.raw', 'wb') as f:
            f.write(self.buffer)
        convert()
        timestamps(self.ts)
        transcription = transcribe(current['datetime'])
        new_log(current['caller'], transcription, current['datetime'], analyze_sentiment(transcription))


def main():
    static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    application = tornado.web.Application([(r"/", MainHandler),
                                            (r"/event", EventHandler),
                                            (r"/ncco", CallHandler),
                                            (r"/socket", WSHandler),
                                            (r'/s/(.*)', tornado.web.StaticFileHandler, {'path': static_path}),
                                        ])
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 80))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
	
	

