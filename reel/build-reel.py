#!/usr/bin/env python3
"""Arma el reel 9:16 de SMART HOME LUXURY a partir de source.mp4 + audio.json (Whisper word timestamps).
Reglas aplicadas (pipeline/MONTAGE-CRAFT.md): texto en pantalla antes de 0.5s, cortes de aire muerto,
punch-ins alternados (pattern-interrupt cada 2-4s), captions karaoke palabra por palabra (highlight #22D3EE),
un solo grade sobre todo, cadena de audio + loudnorm -14 LUFS.
"""
import json, subprocess, sys, os

W = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = "/Users/mac/Desktop/SMART HOME LUXURY/edit"
os.makedirs(OUT_DIR, exist_ok=True)
FFMPEG = "/usr/local/opt/ffmpeg-full/bin/ffmpeg"
SRC = os.path.join(W, "source.mp4")
ASS = os.path.join(W, "captions.ass")
OUT = os.path.join(OUT_DIR, "SMART-HOME-LUXURY-reel.mp4")

# ---- 1. cut list en segundos FUENTE, con zoom (punch-in) por segmento -------------------------------
KEEP = [
    (0.00, 3.40, 1.00),   # "Deja de pagar más por tu aire portátil"
    (5.55, 8.90, 1.10),   # "en Smart Home Luxury eliminamos los intermediarios"
    (8.90, 13.15, 1.00),  # "y te damos el mejor precio ... hasta tu casa"
    (14.45, 19.85, 1.12), # "Aires portátil desde 8500 hasta 13500 BTU"
    (19.85, 24.10, 1.00), # "un año de garantía, incluye envío en todo Santo Domingo"
    (26.10, 28.20, 1.10), # "No importa la hora ni el día"
    (28.20, 32.70, 1.00), # "siempre tendrás respuestas rápidas ... en menos de un minuto"
    (32.70, 34.30, 1.15), # "aquí nadie te desespera"
]

# escenas = cambios de locación; con --xfade se funden 0.4s entre escenas (dentro de una escena: corte seco)
SCENES = [[0], [1, 2], [3, 4], [5, 6, 7]]
PERUANO = "--peruano" in sys.argv  # estilo completo del editor peruano (ver edit/PERUANO-analisis.md)
XFADE = "--xfade" in sys.argv or PERUANO
SHOT = "--shotcraft" in sys.argv   # transiciones renderizadas con Remotion (shotcraft ClockWipe) en trans/t{k}.mp4
XF = 0.6 if SHOT else ((0.3 if PERUANO else 0.4) if XFADE else 0.0)
XFADE_TYPE = "fadewhite" if PERUANO else "fade"   # peruano: flash a blanco en cada cambio de locación
LEAK = "/Users/mac/Desktop/SMART HOME LUXURY/edit/overlays/light-leak-01.mp4" if PERUANO else None
if PERUANO:
    OUT = os.path.join(OUT_DIR, "SMART-HOME-LUXURY-reel-v7-peruano.mp4")
SCENE_OF = {i: k for k, sc in enumerate(SCENES) for i in sc}
if XFADE and not PERUANO:
    OUT = os.path.join(OUT_DIR, "SMART-HOME-LUXURY-reel-v2-xfade.mp4")
if SHOT:
    OUT = os.path.join(OUT_DIR, "SMART-HOME-LUXURY-reel-v3-shotcraft.mp4")

def src_to_out(t):
    """mapa tiempo fuente -> tiempo salida; None si cae en un corte"""
    acc = 0.0
    for i, (a, b, _) in enumerate(KEEP):
        if a <= t <= b:
            return acc + (t - a) - XF * SCENE_OF[i]
        acc += b - a
    return None

TOTAL = sum(b - a for a, b, _ in KEEP) - XF * (len(SCENES) - 1)

# ---- 2. captions karaoke desde las palabras de Whisper ---------------------------------------------
FIX = {"smartphone": "Smart Home", "luxury": "Luxury", "8500": "8,500", "13500": "13,500", "desespera": "esperando."}
d = json.load(open(os.path.join(W, "audio.json")))
words = []
for s in d["segments"]:
    for w in s["words"]:
        txt = w["word"].strip()
        key = txt.strip(",.").lower()
        txt = FIX.get(key, txt)
        so, eo = src_to_out(w["start"]), src_to_out(min(w["end"], w["start"] + 1.2))
        if so is None or eo is None:
            # palabra cortada por el cut list (ej. el "en" fantasma de 3.54-5.74): saltar
            continue
        words.append({"t": txt.upper(), "s": so, "e": max(eo, so + 0.12)})

# grupos de <=3 palabras / <=22 chars, cortando en puntuación
groups, cur = [], []
def flush():
    global cur
    if cur: groups.append(cur); cur = []
for w in words:
    cand = " ".join(x["t"] for x in cur + [w])
    if cur and (len(cur) >= 3 or len(cand) > 22):
        flush()
    cur.append(w)
    if w["t"].endswith((",", ".")):
        flush()
flush()

def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

HI, WHITE, DIM = "&H00EED322", "&H00FFFFFF", "&H00B0B0B0"  # ASS = BGR: #22D3EE -> EED322
# estilo peruano: minúsculas, a media altura (pecho), sin karaoke, palabra clave GRANDE
KEYWORDS = {"smart", "home", "luxury", "8,500", "13,500", "btu", "garantía", "envío", "minuto", "desespera",
            "precio", "intermediarios", "portátil", "portátiles", "esperando"}
STYLE_LINE = (f"Style: Cap,Arial,52,{WHITE},{WHITE},&H00000000,&H80000000,-1,0,0,0,100,100,0.5,0,1,3,3,2,60,60,800,1"
              if PERUANO else
              f"Style: Cap,Arial,72,{WHITE},{WHITE},&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,4,2,2,60,60,470,1")
lines = [
    "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "WrapStyle: 2", "",
    "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
    STYLE_LINE,
    "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
]
if PERUANO:
    # pedido de Nick (2026-09-15): MAYÚSCULAS + karaoke palabra por palabra + resaltado AMARILLO,
    # conservando media altura y palabra clave grande
    HI = "&H0000FFFF"   # amarillo (ASS = BGR)
    FS_N, FS_K = 52, 92
    def word_tag(x, active):
        big = x["t"].strip(",.").lower() in KEYWORDS
        fs = FS_K if big else FS_N
        sc = 108 if active else 100
        return f"{{\\fs{fs}\\fscx{sc}\\fscy{sc}}}"
for gi, g in enumerate(groups):
    g_end = g[-1]["e"] + 0.20  # +200ms tras la última palabra, luego hard-kill
    if gi + 1 < len(groups):   # nunca solapar con el grupo siguiente (libass los apila)
        g_end = min(g_end, groups[gi + 1][0]["s"])
    for i, w in enumerate(g):
        start = w["s"]
        end = g[i + 1]["s"] if i + 1 < len(g) else g_end
        if end <= start: continue
        parts = []
        for j, x in enumerate(g):
            pre = word_tag(x, j == i) if PERUANO else ""
            if j == i:   parts.append(f"{pre}{{\\c{HI}}}{'' if PERUANO else '{\\fscx108\\fscy108}'}{x['t']}{{\\c{WHITE}\\fscx100\\fscy100}}")
            elif j < i:  parts.append(f"{pre}{{\\c{DIM}}}{x['t']}{{\\c{WHITE}}}")
            else:        parts.append(f"{pre}{x['t']}")
        lines.append(f"Dialogue: 0,{ts(start)},{ts(end)},Cap,,0,0,0,,{' '.join(parts)}")
open(ASS, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print(f"captions: {len(words)} palabras, {len(groups)} grupos, duración salida {TOTAL:.2f}s")

# ---- 3. ffmpeg: trim+punch-in por segmento -> concat -> captions -> grade ; audio chain -----------------
fc = []
for i, (a, b, z) in enumerate(KEEP):
    crop = "" if z == 1.0 else f"crop=floor(iw/{z}/2)*2:floor(ih/{z}/2)*2:(iw-iw/{z})/2:(ih-ih/{z})*0.42,scale=1080:1920,"
    if not SHOT:  # en modo shotcraft el video ya está en scenes/s{k}.mp4
        fc.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,{crop}setsar=1,fps=30,format=yuv420p[v{i}]")
    fc.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo[a{i}]")
n = len(KEEP)
extra_inputs = []
if not XFADE and not SHOT:
    fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[vc][ac]")
else:
    # 1) concat dentro de cada escena  2) fundido entre escenas (xfade) o transición Remotion (shotcraft)
    lens = []
    for k, sc in enumerate(SCENES):
        if SHOT:  # el video de las escenas viene ya renderizado en scenes/s{k}.mp4; aquí solo el audio
            fc.append("".join(f"[a{i}]" for i in sc) + f"concat=n={len(sc)}:v=0:a=1[s{k}a]")
        else:
            fc.append("".join(f"[v{i}][a{i}]" for i in sc) + f"concat=n={len(sc)}:v=1:a=1[s{k}v][s{k}a]")
        lens.append(sum(KEEP[i][1] - KEEP[i][0] for i in sc))
    # audio: acrossfade en cada frontera (igual para ambos modos)
    pa = "s0a"
    for k in range(1, len(SCENES)):
        fc.append(f"[{pa}][s{k}a]acrossfade=d={XF}:c1=tri:c2=tri[x{k}a]")
        pa = f"x{k}a"
    fc.append(f"[{pa}]anull[ac]")
    if XFADE:
        pv, acc = "s0v", lens[0]
        for k in range(1, len(SCENES)):
            off = acc - XF
            fc.append(f"[{pv}][s{k}v]xfade=transition={XFADE_TYPE}:duration={XF}:offset={off:.3f}[x{k}v]")
            pv = f"x{k}v"; acc = off + lens[k]
        fc.append(f"[{pv}]null[vc]")
    else:
        # video: escena k recortada XF al inicio (k>0) y al final (k<last) + transición t{k} de 0.6 s en medio
        ns = len(SCENES)
        extra_inputs = [os.path.join(W, "scenes", f"s{k}.mp4") for k in range(ns)] + \
                       [os.path.join(W, "trans", f"t{k}.mp4") for k in range(1, ns)]
        order = []
        for k in range(ns):
            st = XF if k > 0 else 0.0
            en = lens[k] - (XF if k < ns - 1 else 0.0)
            fc.append(f"[{1 + k}:v]trim={st:.3f}:{en:.3f},setpts=PTS-STARTPTS,fps=30,format=yuv420p[c{k}]")
            order.append(f"[c{k}]")
            if k < ns - 1:
                fc.append(f"[{1 + ns + k}:v]trim=0:{XF},setpts=PTS-STARTPTS,scale=1080:1920,fps=30,format=yuv420p[t{k + 1}]")
                order.append(f"[t{k + 1}]")
        fc.append("".join(order) + f"concat=n={len(order)}:v=1:a=0[vc]")
# --endcard <fondo.mp4> [--cta "texto"]: tarjeta de cierre de 3 s con motion background + nombre + oferta + CTA
ENDCARD = sys.argv[sys.argv.index("--endcard") + 1] if "--endcard" in sys.argv else None
CTA = sys.argv[sys.argv.index("--cta") + 1] if "--cta" in sys.argv else "Escríbenos por WhatsApp"
EC_DUR = 3.0
if ENDCARD:
    OUT = OUT.replace(".mp4", "-cta.mp4")
    ec_idx = 1 + len(extra_inputs)
    extra_inputs.append(ENDCARD)
    FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    def dt(text, size, y, color, start):
        t = text.replace("\\", "\\\\").replace("'", "\\'").replace(":", "\\:")
        return (f"drawtext=fontfile='{FONT}':text='{t}':fontsize={size}:fontcolor={color}:x=(w-text_w)/2:y={y}"
                f":alpha='if(lt(t,{start}),0,min(1,(t-{start})/0.35))':shadowcolor=black@0.6:shadowx=0:shadowy=3")
    ec = (f"[{ec_idx}:v]trim=0:{EC_DUR},setpts=PTS-STARTPTS,"
          f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p,"
          f"eq=brightness=-0.08,"
          + dt("SMART HOME LUXURY", 92, 760, "white", 0.25) + ","
          + dt("Aires portátiles · Envío en todo Santo Domingo", 40, 890, "0xDDDDDD", 0.55) + ","
          + dt(CTA, 60, 1010, "0x22D3EE", 0.85) + ","
          f"fade=t=in:st=0:d=0.3,fade=t=out:st={EC_DUR - 0.4}:d=0.4[ec]")
    fc.append(ec)
    fc.append("[vc][ec]concat=n=2:v=1:a=0[vc2]")
    fc.append(f"[ac]apad=pad_dur={EC_DUR}[ac2]")
    VC, AC = "[vc2]", "[ac2]"  # la cadena posterior (LUT/captions/grade y audio) consume estos
else:
    VC, AC = "[vc]", "[ac]"
# burst cálido (light leak en screen) al entrar a la última locación, como el editor peruano al salir del B-roll
if PERUANO and LEAK and os.path.exists(LEAK):
    lk_idx = 1 + len(extra_inputs)
    extra_inputs.append(LEAK)
    lens_sc = [sum(KEEP[i][1] - KEEP[i][0] for i in sc) for sc in SCENES]
    tB = sum(lens_sc[:3]) - XF * 3 + XF / 2   # centro del último cambio de locación (tiempo de salida)
    t0, dur = tB - 0.12, 0.26
    # leak recortado a 0.26 s, con fade, rellenado con negro antes/después (screen con negro = sin cambio)
    fc.append(f"[{lk_idx}:v]trim=1.2:{1.2 + dur:.3f},setpts=PTS-STARTPTS,"
              f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p,"
              f"fade=t=in:st=0:d=0.08,fade=t=out:st={dur - 0.1:.3f}:d=0.1,"
              f"tpad=start_duration={t0:.3f}:stop_mode=add:stop_duration=90:color=black[lk]")
    fc.append(f"{VC}[lk]blend=all_mode=screen:all_opacity=0.65:shortest=1[vlk]")
    VC = "[vlk]"
grade = "eq=contrast=1.06:saturation=0.92:brightness=-0.02,vignette=angle=PI/5"
# --lut <archivo.cube> [--lut-strength 0.7]: LUT creativo a nivel de timeline (MONTAGE-CRAFT §17), mezclado al % dado
LUT = sys.argv[sys.argv.index("--lut") + 1] if "--lut" in sys.argv else None
LUT_STR = float(sys.argv[sys.argv.index("--lut-strength") + 1]) if "--lut-strength" in sys.argv else 0.7
if LUT:
    OUT = OUT.replace(".mp4", "-lut.mp4")
    lut_esc = LUT.replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
    fc.append(f"{VC}split[g0][g1];[g1]lut3d='{lut_esc}'[gl];[g0][gl]blend=all_mode=normal:all_opacity={LUT_STR}[vg]")
    fc.append(f"[vg]ass='{ASS}',{grade},format=yuv420p[vout]")
else:
    fc.append(f"{VC}ass='{ASS}',{grade},format=yuv420p[vout]")
audio = ("highpass=f=80,equalizer=f=500:t=q:w=1.2:g=-2,equalizer=f=3500:t=q:w=1:g=2.5,"
         "acompressor=threshold=-18dB:ratio=3:attack=5:release=20,alimiter=limit=-1.5dB,"
         "loudnorm=I=-14:TP=-1.5:LRA=11")
fc.append(f"{AC}{audio}[aout]")

cmd = [FFMPEG, "-y", "-v", "error", "-stats", "-i", SRC]
for p in extra_inputs: cmd += ["-i", p]
cmd += ["-filter_complex", ";".join(fc),
       "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
       "-r", "30", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT]
print("render ->", OUT)
r = subprocess.run(cmd)
sys.exit(r.returncode)
