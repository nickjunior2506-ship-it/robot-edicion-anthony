# Robot de edición — Anthony

Pipeline local ($0, sin nube) para convertir tomas verticales de iPhone en un reel de venta 9:16 listo para publicar.
Construido sobre ffmpeg-full (libass) + Whisper local + Remotion. Probado en Mac Intel (i9, solo CPU).

## Qué hace `reel/build-reel.py`
1. Une las tomas, corta el aire muerto (lista `KEEP` en segundos fuente) y alterna punch-ins.
2. Captions karaoke palabra por palabra desde `audio.json` de Whisper (`--word_timestamps True`).
3. Transiciones: corte seco (default), `--xfade` (crossfade 0.4 s), `--shotcraft` (transición Remotion), `--peruano` (flash a blanco + light leak + captions a media altura en MAYÚSCULAS con karaoke amarillo).
4. Color: `--lut archivo.cube --lut-strength 0.7` (un solo grade sobre todo).
5. Cierre opcional: `--endcard fondo.mp4 --cta "texto"`.
6. Audio: pasa altos, presencia, compresor, limitador, `loudnorm` a −14 LUFS.

```bash
# 1) transcribir
ffmpeg -i source.mp4 -vn -ar 16000 -ac 1 audio.wav
whisper audio.wav --model small --language es --word_timestamps True --output_format all
# 2) renderizar
python3 build-reel.py --peruano --lut ../luts/peruano-B-dia.cube --lut-strength 0.7
```
Las rutas de salida/fondos están fijas en el script (`OUT_DIR`, `LEAK`): ajustarlas al clonar.

## `reel/lookmatch.py` — extraer el look de un video de referencia como LUT
Transferencia de color estadística (Reinhard) en Lab; conserva la exposición propia y copia contraste, casta y saturación.
```bash
ffmpeg -i referencia.mp4 -vf "fps=2,scale=96:170" -f rawvideo -pix_fmt rgb24 ref.rgb
ffmpeg -i mio.mp4        -vf "fps=2,scale=96:170" -f rawvideo -pix_fmt rgb24 src.rgb
python3 lookmatch.py ref.rgb src.rgb 96 170 look.cube nombre
```
`luts/peruano-*.cube` son dos looks extraídos así. `reel/PERUANO-analisis.md` es el desglose de transiciones y estilo de esos videos.

## `remotion/` — transición de video real en 9:16
`ClockWipeReal.tsx` adapta el ClockWipe de shotcraft (AI Video Studio Kit) a dos clips reales (`OffthreadVideo`).
Copiar a `shotcraft/template/src/` y renderizar: `npx remotion render src/shl.ts ClockWipeReal out.mp4 --props='{"a":"shl/t1a.mp4","b":"shl/t1b.mp4"}'`.

## `docs/` — la doctrina del robot
Estilos que venden, recetario táctico (fuentes, colores, transiciones permitidas, SFX), knowledge base y mapa de robots del mercado.

## Requisitos
`brew install ffmpeg-full yt-dlp` · `pipx install openai-whisper --python python3.12 --pip-args="--prefer-binary"` (+ `numpy<2`) · Node 18+ para Remotion.

---

## Créditos e identificación

| | |
|---|---|
| **Proyecto** | REA — Robot de Edición Anthony |
| **Versión** | v1.0.1 (2026-09-16) |
| **Autor** | Anthony Junior Susaña Ramírez |
| **Contacto** | WhatsApp +1 (849) 517-8351 · [wa.me/18495178351](https://wa.me/18495178351) |
| **Repositorio original** | https://github.com/nickjunior2506-ship-it/robot-edicion-anthony |
| **Licencia** | **Uso NO comercial** (ver `LICENSE`). Uso personal/educativo permitido con atribución. **Uso comercial prohibido sin permiso escrito de Anthony Junior Susaña Ramírez** (WhatsApp 849-517-8351). |

Cada archivo fuente lleva esta cabecera y los scripts Python exponen `__author__`, `__contact__`, `__version__` y `__project__`.
