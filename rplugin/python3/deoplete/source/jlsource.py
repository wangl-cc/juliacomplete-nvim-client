from deoplete.base.source import Base
from JLVim.jlclient import JLVimClient

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'juliatools'
        self.mark = '[JL]'
        self.rank = 1000
        self.filetypes = ["julia"]

    def gather_candidates(self, context):
        jlcompcandidate = self.vim.call('juliadeompleteadapter#GetCompletions')
        return jlcompcandidate
