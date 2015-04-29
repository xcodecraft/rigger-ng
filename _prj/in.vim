set nowrap
set encoding=utf-8
set fileencoding=utf-8
set background=dark
set nu

noremap <F2> <Esc>:! /home/q/tools/pylon_rigger/rigger start -s test <CR>
set errorformat=%m\ in\ %f\ on\ line\ %l 
call Probe_ide_init("$HOME/devspace/weber")
au! BufRead,BufNewFile *.html setfiletype php

func! ReloadPrjide()
    if bufname('%') !~ '\.prjide'
        return
    endif 
    :!/home/q/tools/game_team/bin/reloadprjide.sh .
endf

noremap \F : call ReloadPrjide() <CR> <CR>
