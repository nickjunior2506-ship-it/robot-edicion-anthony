#!/bin/bash
# ============================================================
#  Robot de Edición Anthony (REA) · v1.0.0
#  Autor:    Anthony
#  Contacto: WhatsApp +1 (849) 517-8351 · https://wa.me/18495178351
#  Repo:     https://github.com/nickjunior2506-ship-it/robot-edicion-anthony
#  Licencia: MIT (ver LICENSE). Si lo usas o modificas, conserva este crédito.
# ============================================================
set -e
export PATH="/usr/local/opt/ffmpeg-full/bin:$PATH"
SRC="/Users/mac/Desktop/SMART HOME LUXURY"
CLIPS="/Users/mac/robot-de-edicion/salida/smart-home-luxury"
OUT="$CLIPS/anuncio"; mkdir -p "$OUT/seg"; cd "$OUT"
# Layer 3: reframe cada toma a 9:16 1080x1920 30fps (crop central), audio 48k
i=0; : > concat.txt; : > offsets.txt; off=0
for f in IMG_5437.mov IMG_5438.MOV IMG_5439.MOV IMG_5440.MOV; do
  i=$((i+1)); seg="seg/$(printf %02d $i).mp4"
  ffmpeg -y -v error -i "$SRC/$f" -vf "crop=ih*9/16:ih,scale=1080:1920,fps=30,format=yuv420p" \
    -c:v libx264 -preset fast -crf 18 -c:a aac -ar 48000 -b:a 192k "$seg"
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$seg")
  echo "file '$seg'" >> concat.txt; echo "${f%.*} $off $d" >> offsets.txt
  off=$(python3 -c "print($off+$d)")
done
ffmpeg -y -v error -f concat -safe 0 -i concat.txt -c copy assembled.mp4
# Layer 2: un solo SRT con offsets + corrección de marca
python3 - <<'PY'
lines=[l.split() for l in open('offsets.txt')]
def t2s(t): h,m,s=t.replace(',','.').split(':'); return int(h)*3600+int(m)*60+float(s)
def s2t(s): h=int(s//3600); m=int(s%3600//60); x=s%60; return f"{h:02d}:{m:02d}:{int(x):02d},{int(round((x-int(x))*1000)):03d}"
n=0; out=[]
for name,off,dur in lines:
    off=float(off); txt=open(f'../{name}/transcript.srt').read().replace('Smartphone Luxury','Smart Home Luxury')
    for blk in txt.strip().split('\n\n'):
        ls=blk.split('\n')
        if len(ls)<3: continue
        a,b=ls[1].split(' --> ')
        text=' '.join(ls[2:]); words=text.split()
        # partir en grupos de <=28 caracteres (1-2 lineas cortas), tiempo proporcional a caracteres
        groups=[]; cur=''
        for w in words:
            if cur and len(cur)+1+len(w)>28: groups.append(cur); cur=w
            else: cur=(cur+' '+w).strip()
        if cur: groups.append(cur)
        t0=t2s(a)+off; t1=t2s(b)+off; total=sum(len(g) for g in groups) or 1; t=t0
        for g in groups:
            dur=(t1-t0)*len(g)/total; n+=1
            out.append(f"{n}\n{s2t(t)} --> {s2t(t+dur)}\n{g}\n"); t+=dur
open('captions.srt','w').write('\n'.join(out))
PY
# Loudnorm 2 pasos a -14 LUFS / TP -1 (medir -> aplicar)
M=$(ffmpeg -v info -i assembled.mp4 -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
II=$(echo "$M"|python3 -c "import json,sys;d=json.load(sys.stdin);print(d['input_i'],d['input_tp'],d['input_lra'],d['input_thresh'],d['target_offset'])")
read ii itp ilra ith toff <<<"$II"
STYLE="FontName=Avenir Next Heavy,FontSize=17,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2.5,Shadow=1,Alignment=2,MarginV=85,MarginL=28,MarginR=28,Bold=1"
# Export final: H.264 High L4.2, 30fps, 12 Mbps, captions quemados
ffmpeg -y -v error -i assembled.mp4 \
  -vf "subtitles=captions.srt:force_style='$STYLE'" \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$ii:measured_TP=$itp:measured_LRA=$ilra:measured_thresh=$ith:offset=$toff:linear=true" \
  -c:v libx264 -profile:v high -level 4.2 -preset medium -b:v 12M -maxrate 15M -bufsize 24M -r 30 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart smart-home-luxury-9x16.mp4
echo "=== QA ==="
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,codec_name,profile,level,r_frame_rate,bit_rate:format=duration -of default=nw=1 smart-home-luxury-9x16.mp4
ffmpeg -v info -i smart-home-luxury-9x16.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -A8 "Summary" | grep -E "I:|Peak:|LRA:"
echo "=== CAPTIONS ==="
cat captions.srt
