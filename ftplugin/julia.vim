if !exists("g:julia_comment_symbol")
    let julia_comment_symbol = '#'
endif

augroup JLComInit
    autocmd!
    autocmd VimEnter *.jl :call JLComInit()
augroup END

nnoremap <buffer> <leader>/ :call comment#Comment(julia_comment_symbol)<cr>
nnoremap <buffer> <leader>d :call juliadocstring#JuliaDocstring()<cr>
nnoremap <buffer> <leader>l :call JLRunLine()<cr>
nnoremap <buffer> <leader>b :call JLRunBlock()<cr>

setlocal completefunc=juliacomplete#CompleteServer

