#!/usr/bin/env bash

OUT="noise_merge_frames"
mkdir -p "$OUT"
rm -f "$OUT"/frame_*.png

W=1080
H=1920
N=1000

ALPHA=0.87
BETA=0.13

prev=""

for i in $(seq -w 0 $((N-1))); do
    frame="$OUT/frame_$i.png"

    if [ -z "$prev" ]; then
        gmic $W,$H,1,3,u\(255\) -o "$frame"
    else
        gmic "$prev" \
            $W,$H,1,3,u\(255\) \
            -mul[0] $ALPHA \
            -mul[1] $BETA \
            -add[0] [1] \
            -keep[0] \
            -blur 10 \
            -equalize 128 \
            -o "$frame"
    fi

    prev="$frame"
    echo "made $frame"
done

#ffmpeg -framerate 30 -i "$OUT/frame_%03d.png" -c:v libx264 -pix_fmt yuv420p noise_merge4.mp4

mkdir -p cartoon_frames
rm -f cartoon_frames/frame_*.png

x=0
y=0

for f in "$OUT"/*.png; do

    x=$(( x + RANDOM % 3 - 1 ))
    y=$(( y + RANDOM % 3 - 1 ))

    gmic "$f" \
        -cartoon 7,47,20,0.01,0.71,240 \
        -shift $x,$y,0,0,2 \
        -o "cartoon_frames/$(basename "$f")"

done

ffmpeg -framerate 20 -i cartoon_frames/frame_%03d.png \
  -c:v libx264 -pix_fmt yuv420p ca1.mp4
  

