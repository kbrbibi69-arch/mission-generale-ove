#!/usr/bin/env bash
# Version sans humour seule : voix off -16 LUFS, musique -31 LUFS (durée propre à la variante).
set -euo pipefail
cd "$(dirname "$0")/../.."
ffmpeg -hide_banner -loglevel error -y -i assets/audio/voix-off-sobre.wav \
  -af "highpass=f=70,equalizer=f=3200:t=q:w=1.1:g=2,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-16:TP=-1.5:LRA=9" \
  -ar 44100 -ac 1 .media/vo-sobre.wav
mv .media/vo-sobre.wav assets/audio/voix-off-sobre.wav
ffmpeg -hide_banner -loglevel error -y -i .media/music-raw-sobre.wav \
  -af "lowpass=f=5200,highpass=f=40,loudnorm=I=-31:TP=-6:LRA=11" -ar 44100 -b:a 192k assets/audio/musique-sobre.mp3
