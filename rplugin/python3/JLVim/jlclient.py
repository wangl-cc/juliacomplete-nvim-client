import socket
import json
from io import StringIO


def json_recv(sock):
    buf = StringIO()
    while True:
        msg = sock.recv(3072).decode('utf-8')
        buf.write(msg)
        if '\n' in buf.getvalue():
            break
    return json.loads(buf.getvalue())


def json_send(sock, *args):
    msg = bytes(json.dumps(args), "utf-8")
    sock.sendall(msg)


class JLVimClient():

    def __init__(self, host="localhost", port=18888):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.host = host
        self.callbackID = 1

    def connect(self):
        self.sock.connect((self.host, self.port))

    def close(self):
        self.sock.close()

    def rpc(self, t, *args, cd=True):
        if cd:
            t = {"type": t, "callback": self.callbackID}
            self.callbackID += 1
        json_send(self.sock, t, *args)
        return json_recv(self.sock)

    def getcompletions(self, line, force, path=None, mod=None):
        d = {"line": line, "force": force}
        if not path is None:
            d["path"] = path
        if not mod is None:
            d["mod"] = mod
        cd, cdID, compdict = self.rpc("completions", d)
        comps = compdict['completions']
        return [{'word': comp["text"], 'kind':comp["type"]} for comp in comps]

    def getmethods(self, word, mod=None):
        d = {"word": word}
        if not mod is None:
            d["mod"] = mod
        cd, cdID, methodsdict = self.rpc("methods", d)
        if methodsdict.get("error",  False):
            return "Some error happen!"
        else:
            return methodsdict['items']

    def getworkspace(self, mod="Main"):
        cd, cdID, contexts = self.rpc("workspace", mod)
        workspace = []
        for c in contexts:
            context = c['context']
            for i in c['items']:
                if context == 'Main':
                    workspace.append({'type': i['type'],
                                      'name': i['name'],
                                      'value': i['value']['contents']})
                else:
                    workspace.append({'type': i['type'],
                                      'name': '{}.{}'.format(context, i['name']),
                                      'value': i['value']['contents']})
        return workspace
