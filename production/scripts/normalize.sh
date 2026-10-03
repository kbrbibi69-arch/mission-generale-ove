#!/usr/bin/env bash
# Niveaux : voix off -16 LUFS, musique -31 LUFS (lit sonore sous la voix).
set -euo pipefail
cd "$(dirname "$0")/../.."
for v in humour sobre; do
  ffmpeg -hide_banner -loglevel error -y -i assets/audio/voix-off-$v.wav \
    -af "highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-16:TP=-1.5:LRA=9" \
    -ar 44100 -ac 1 .media/vo-$v.wav
  mv .media/vo-$v.wav assets/audio/voix-off-$v.wav
done
ffmpeg -hide_banner -loglevel error -y -i .media/music-raw.wav \
  -af "lowpass=f=5200,highpass=f=40,loudnorm=I=-31:TP=-6:LRA=11" -ar 44100 -b:a 192k assets/audio/musique-ove.mp3
for f in assets/audio/*; do echo "$f"; ffmpeg -hide_banner -i "$f" -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1; done
