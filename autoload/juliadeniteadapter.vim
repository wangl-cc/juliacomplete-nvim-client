function! juliadeniteadapter#GetWorkSpace(mod)
    call JLGetWorkspace(a:mod)
    return g:jlworkspace
endfunc

function! juliadeniteadapter#GetMethods()
    call JLGetMethods()
    return g:jlmethods
endfunc