import pynvim
from time import sleep
import json
from JLVim.jlclient import JLVimClient

JL_SEPARATOR = (' ', ',', ';', ':', '"', "'", '/', '?', '\\', '|', '<', '>', )

@pynvim.plugin
class JLVim():

    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.function('JLVimInit', sync=False)
    def init_wrap(self, args):
        self.init_local(*args)

    def init_local(self, repl_height=10, host="localhost", port=18888):
        self.host = host
        self.port = port
        beginwindow = self.nvim.current.window
        self.nvim.command(
            '{} split term://.//julia --startup-file=no -i -e \\"using Atom; Atom.serve({}) \\"'.format(repl_height, self.port))
        self.nvim.current.buffer.name = "julia"
        self.jlbuffer = self.nvim.current.buffer
        self.nvim.current.window = beginwindow
        client = JLVimClient(self.host, self.port)
        self.client = client
        sleep(3)
        self.client.connect()

    # @pynvim.function("Reconnect")
    # def reconnect(self, args):
    #     try:
    #         # Just for test, it's junk message
    #         msg = json.dumps(["-e", "1"])
    #         msg = bytes(msg, "utf-8")
    #         self.sock.sendall(msg)
    #         _ = json_recv(self.sock)
    #     except:
    #         if not self.jlbuffer.valid:
    #             self.nvim.command(
    #                 '10 split term://.//julia --startup-file=no -L {}'.format(os.path.join(os.path.abspath(__file__), '../../../julia/loadfile.jl')))
    #             self.nvim.current.buffer.name = "julia"
    #             sleep(3)
    #         self.sock.connect((self.host, self.port))

    # @pynvim.function('JLFindStart', sync=True)
    # def findstart(self, args):
    #     line = self.nvim.current.line
    #     _, col = self.nvim.current.window.cursor
    #     col -= 1
    #     jlcompstart = findstart(line, col)
    #     self.nvim.command("let g:jlcompstart={}".format(jlcompstart))

    @pynvim.function('JLGetCompletions', sync=True)
    def jlcompget(self, args):
        line = self.nvim.current.line
        jlcompcandidate = self.client.getcompletions(line, 1)
        self.nvim.command(
            "let g:jlcompcandidate={}".format(json.dumps(jlcompcandidate)))

    @pynvim.function('JLGetMethods', sync=True)
    def jlgetmethods(self, args):
        line = self.nvim.current.line
        row, col = self.nvim.current.window.cursor
        start = 0
        end = len(line)
        for i in range(col-1, -1, -1):
            if line[i] in JL_SEPARATOR:
                start = i
                break
        for i in range(col-1, len(line), 1):
            if line[i] in JL_SEPARATOR:
                end = i+1
                break
        methods = self.client.getmethods(line[start, end])
        self.nvim.command(
            "let g:jlmethods={}".format(json.dumps(methods)))

    @pynvim.function('JLGetWorkspace', sync=True)
    def jlgetworkspace(self, args):
        mod = args[0][0]
        workspace = self.client.getworkspace(mod)
        self.nvim.command(
            "let g:jlworkspace={}".format(json.dumps(workspace)))
    
    # @pynvim.function('JLRunLine')
    # def jlrunline(self, args):
    #     line = self.nvim.current.line
    #     msg = json.dumps(["-e", line])
    #     msg = bytes(msg, "utf-8")
    #     self.sock.sendall(msg)
    #     recv = json_recv(self.sock).decode("utf-8")
    #     self.nvim.command("echo {}".format(recv))

    # @pynvim.function('JLRunBlock')
    # def jlrunblock(self, args):
    #     row, _ = self.nvim.current.window.cursor
    #     beginrow = row
    #     endrow = row
    #     for i in range(row, 1, -1):
    #         line = self.nvim.eval("getline({})".format(i))
    #         if line[0] != " " and line[0:3] != "end":
    #             beginrow = i
    #             break
    #     i = row
    #     while True:
    #         line = self.nvim.eval("getline({})".format(i))
    #         if line[0:3] == "end":
    #             endrow = i
    #             break
    #         i += 1
    #     lines = self.nvim.eval("getline({}, {})".format(beginrow, endrow))
    #     block = "\n".join(lines)
    #     msg = json.dumps(["-e", block])
    #     msg = bytes(msg, "utf-8")
    #     self.sock.sendall(msg)
    #     recv = json_recv(self.sock).decode("utf-8")
    #     self.nvim.command("echo {}".format(recv))

    @pynvim.autocmd('VimLeavePre', pattern='*.jl', sync=True)
    def vimleave(self, args):
        self.close()

    def close(self):
        self.nvim.close()
        self.client.close()
