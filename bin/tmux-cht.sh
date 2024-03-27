#!/usr/bin/env bash
prefix="$HOME/software/dotfiles/tmux/"
# command_list=$(which .tmux-cht-command)
command_list="$prefix/.tmux-cht-command"
lang_list="$prefix/.tmux-cht-languages"
# lang_list=$(which tmux-cht-languages)
# selected=`cat ~/.tmux-cht-languages ~/.tmux-cht-command | fzf`
selected=`cat $lang_list $command_list | fzf`
if [[ -z $selected ]]; then
    exit 0
fi

read -p "Enter Query: " query

if grep -qs "$selected" ~/.tmux-cht-languages; then
    query=`echo $query | tr ' ' '+'`
    tmux neww bash -c "echo \"curl cht.sh/$selected/$query/\" & curl cht.sh/$selected/$query & while [ : ]; do sleep 1; done"
else
    tmux neww bash -c "curl -s cht.sh/$selected~$query | less -R"
fi
