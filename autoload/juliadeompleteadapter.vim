function! juliadeompleteadapter#GetCompletions()
    call JLGetCompletions()
    return g:jlcompcandidate
endfunction

