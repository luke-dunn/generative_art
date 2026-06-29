# apply cartoon in second pass

mkdir -p cartoon_frames3
rm -f cartoon_frames3/frame_*.png


for f in frames/*.png; do
    gmic "$f" \
        -cartoon 7.72,17.6,15.9,0.168,2.73,247 \
        -o "cartoon_frames3/$(basename "$f")"
done


ffmpeg -y -framerate 20 -i cartoon_frames3/frame_%04d.png \
  -c:v libx264 -pix_fmt yuv420p animals06.mp4
  

