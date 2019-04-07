# from denite.base.source import Base


# class Source(Base):

#     def __init__(self, vim):
#         super().__init__(vim)

#         self.name = 'jlworksapce'
#         self.kind = 'base'

#     def gather_candidates(self, context):
#         orkspace = self.vim.call('juliadeniteadapter#GetWorkSpace', 'Main')
#         candidates = []
#         for i in workspace:
#             candidates.append({
#                 'word': '{name}={value}\t{type}'.format(**i)
#             })
#         return candidates
