augroup JLComInit
    autocmd!
    autocmd VimEnter *.jl :call JLComInit()
    autocmd VimEnter *.jl :1 wincmd w
augroup END

setlocal completefunc=juliacomplete#CompleteServer
