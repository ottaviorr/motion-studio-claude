#!/bin/bash
# grade.sh saida.jpg img1 img2 ... → folha de conferência (2 por linha, 960x540 cada). Rodar com bash (no zsh a lista não se divide).
o=$1; shift; n=$#; args=(); fc=""; i=0
for f in "$@"; do args+=(-i "$f"); fc+="[$i]scale=960:540[s$i];"; i=$((i+1)); done
if [ $((n%2)) = 1 ]; then args+=(-f lavfi -i color=black:960x540); fc+="[$i]null[s$i];"; n=$((n+1)); fi
rows=""; r=0; for ((k=0;k<n;k+=2)); do fc+="[s$k][s$((k+1))]hstack[r$r];"; rows+="[r$r]"; r=$((r+1)); done
if [ $r = 1 ]; then fc+="${rows}null"; else fc+="${rows}vstack=inputs=$r"; fi
ffmpeg -v error -y "${args[@]}" -filter_complex "$fc" -frames:v 1 "$o"
