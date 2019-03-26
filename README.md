# juliacomplete-nvim-client

A simple plug-in for nvim support [Julia](https://julialang.org/).

## Feature

1. Julia REPLCompletion based completion.
2. Eval code in current line or current block and get its result.
3. Docstring generation. Support from [AtsushiSakai/julia.vim](https://github.com/AtsushiSakai/julia.vim)
4. Quick comment.

## Installation

### 1. Install [wangl-cc/VimCompletion.jl](https://github.com/wangl-cc/VimCompletion.jl).

### 2. Install this plug-in.

#### Installation with Vim-Plug
```
Plug 'wangl-cc/juliacomplete-nvim-client', { 'do' : ':UpdateRemotePlugins' }
```

## Usage

### 1. Completion

Because the official [julia-vim](https://github.com/JuliaEditorSupport/julia-vim) plug-in uses the `omnifunc` as its complete method, this plug-in uses `completefunc` as complete method wich is used for Insert mode completion with `CTRL-X CTRL-U`.

### 2. Eval code

Like [Juno](http://junolab.org/) this plug-in can send code to term split (open default, if you exit, completion and eval code would be disable then you should `call Reconnect()`) and eval it then display its result (not inline but by echo). There are two functions: `JLRunLine` and `JLRunBlock` to eval code in current line and current block. Map your own shortcut to use this feature.

### 3. Docstring generation

There is a function `juliadocstring#JuliaDocstring` being used to generate docstring. Map your own shortcut as above.

### 4. Quick comment

There is a function `comment#Comment(julia_comment_symbol)` being used to comment and remove comment. Map your own shortcut as above.

### Example

Here is an example of file `~/.vim/ftplugin/julia.vim`:

```vimscript
if !exists("g:julia_comment_symbol")
    let julia_comment_symbol = '#'
endif

" key map
nnoremap <buffer> <leader>l :call JLRunLine()<cr>
nnoremap <buffer> <leader>b :call JLRunBlock()<cr>
nnoremap <buffer> <leader>/ :call comment#Comment(julia_comment_symbol)<cr>
nnoremap <buffer> <leader>d :call juliadocstring#JuliaDocstring()<cr>

" autoclose
augroup JuliaAutoClose
    autocmd!
    autocmd bufenter * if (winnr("$") == 1 && bufname("$") =~ "term://.//.*:julia -L .*")| q | endif
augroup END
```
