function! juliacomplete#CompleteServer(findstart, base)
    if a:findstart
        call JLFindStart()
        return g:jlcompstart
    else
        call JLComGet(a:base)
        return g:jlcomp
endfunction

