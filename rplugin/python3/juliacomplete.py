import pynvim
import socket
import json
import os
import time


def findstart(line, pos):
    if pos == 0:
        return 0
    line = line[0:pos]
    findusing = line.rfind("using ")
    findimport = line.rfind("import ")
    for i in range(pos-1, -1, -1):
        if line[i] in (' ', '(', ')', '[', ']', '{', '}', '=', '!', '+', '-', '+', '*', '&', '#', '$', '%', '^', '<', '>', '?', ',', ':', ';'):
            if line[i] == ' ':
                if i == findusing+5:
                    return findusing
                elif i == findimport+6:
                    return findimport
                else:
                    return i+1
            else:
                return i+1
    return 0


def json_recv(sock):
    start = sock.recv(1)
    if start == b'[':
        end = b']'
    elif start == b'{':
        end = b'}'
    else:
        return start
    count = 1
    json_string = start
    while count > 0:
        char = sock.recv(1)
        if char == start:
            count += 1
        elif char == end:
            count -= 1
        json_string += char
    return json_string


@pynvim.plugin
class JuliaCompletePlugin(object):

    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.function('JLComInit', sync=False)
    def init_wrap(self, args):
        self.init(*args)

    def init(self, host="localhost", port=18888):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock
        self.host = host
        self.port = port
        beginwindow = self.nvim.current.window
        self.nvim.command(
            '10 split term://.//julia --startup-file=no -L {}'.format(os.path.join(os.path.abspath(__file__), '../../../julia/loadfile.jl')))
        self.nvim.current.buffer.name = "julia"
        self.jlbuffer = self.nvim.current.buffer
        self.nvim.current.window = beginwindow
        time.sleep(3)
        self.sock.connect((self.host, self.port))

    @pynvim.function("Reconnect")
    def reconnect(self, args):
        try:
            # Just for test, it's junk message
            msg = json.dumps(["-e", "1"])
            msg = bytes(msg, "utf-8")
            self.sock.sendall(msg)
            _ = json_recv(self.sock)
        except:
            if not self.jlbuffer.valid:
                self.nvim.command(
                    '10 split term://.//julia --startup-file=no -L {}'.format(os.path.join(os.path.abspath(__file__), '../../../julia/loadfile.jl')))
                self.nvim.current.buffer.name = "julia"
                time.sleep(3)
            self.sock.connect((self.host, self.port))

    @pynvim.function('JLFindStart', sync=True)
    def findstart(self, args):
        line = self.nvim.current.line
        _, col = self.nvim.current.window.cursor
        col -= 1
        jlcompstart = findstart(line, col)
        self.nvim.command("let g:jlcompstart={}".format(jlcompstart))

    @pynvim.function('JLComGet', sync=True)
    def jlcompget(self, args):
        base = args[0]
        msg = json.dumps(["-c", base, len(base)])
        msg = bytes(msg, "UTF-8")
        self.sock.sendall(msg)
        recv = json_recv(self.sock).decode("utf-8")
        self.nvim.command("let g:jlcomp={}".format(recv))

    @pynvim.function('JLRunLine')
    def jlrunline(self, args):
        line = self.nvim.current.line
        msg = json.dumps(["-e", line])
        msg = bytes(msg, "utf-8")
        self.sock.sendall(msg)
        recv = json_recv(self.sock).decode("utf-8")
        self.nvim.command("echo {}".format(recv))

    @pynvim.function('JLRunBlock')
    def jlrunblock(self, args):
        row, _ = self.nvim.current.window.cursor
        beginrow = row
        endrow = row
        for i in range(row, 1, -1):
            line = self.nvim.eval("getline({})".format(i))
            if line[0] != " " and line[0:3] != "end":
                beginrow = i
                break
        i = row
        while True:
            line = self.nvim.eval("getline({})".format(i))
            if line[0:3] == "end":
                endrow = i
                break
            i += 1
        lines = self.nvim.eval("getline({}, {})".format(beginrow, endrow))
        block = "\n".join(lines)
        msg = json.dumps(["-e", block])
        msg = bytes(msg, "utf-8")
        self.sock.sendall(msg)
        recv = json_recv(self.sock).decode("utf-8")
        self.nvim.command("echo {}".format(recv))

    @pynvim.autocmd('VimLeavePre', pattern='*.jl', sync=True)
    def vimleave(self, args):
        self.close()

    def close(self):
        self.nvim.close()
        self.sock.close()
