augroup JLComInit
    autocmd!
    autocmd VimEnter *.jl :call JLComInit()
augroup END

setlocal completefunc=juliacomplete#CompleteServer
