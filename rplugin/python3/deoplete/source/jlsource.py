from deoplete.base.source import Base
from deoplete.util import convert2candidates


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


class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'juliatools'
        self.mark = '[JL]'
        self.rank = 1000
        self.filetypes = ["julia"]

    def get_complete_position(self, context):
        line = context['input']
        return findstart(line, len(line))

    def gather_candidates(self, context):
        base = context['input'][context['complete_position']:context['position'][2]-1]
        l = self.vim.call('juliacomplete#CompleteServer', 0, base)
        return convert2candidates(l)
