# Análisis de los videos de referencia (~/Desktop/PERUANO) — 2026-09-15

Dos reels verticales 1080×1920 @30 fps ya editados: `4v.mp4` (37 s, vendedor de iPhone, noche) y
`ATENCION EMPRESARIO FINAL.mp4` (51 s, agencia WhatsApp, día). Analizados fotograma a fotograma.

## Transiciones que usa (catálogo verificado en los cortes detectados)
| Tipo | Dónde | Cómo replicarlo en build-reel.py |
|---|---|---|
| **Corte seco** (dominante) | todos los cambios de plano/ángulo: a@11.3, 23.0, 28.8, 31.7 · b@6.9, 10.5, 18.0, 27.1, 32.2, 48.2 | ya está (v1) |
| **Flash a blanco** (dip to white, ~0.3 s) | cambios de locación: b@22.2, b@39.9; a@24.0 al entrar el B-roll | pendiente: `xfade=transition=fadewhite:duration=0.3` |
| **Flash cálido / light-leak burst** (~0.25 s) | a@26.0 al volver del B-roll al presentador | pendiente: light leak de la carpeta Overlays en screen 60 % solo 6-8 fotogramas |
| **Zoom/whip con motion blur** | dentro del B-roll de pantalla de celular (a@24.6, 25.1) | no aplica a talking-head; sería para B-roll |
| **Punch-in por frase** (escala 1.0 → ~1.1-1.2) | cada 1-3 s en ambos videos | ya está (KEEP[].zoom) |

## Captions
1-3 palabras por grupo, blanco bold sans con sombra, centradas **a media altura** (pecho), no abajo. Palabras clave
más grandes ("más inteligentes", "SÍ SE NOTA", "alta gama", "Vender", "tarde"). Nuestro build-reel.py ya hace grupos
de ≤3 palabras; diferencias: ellos usan minúsculas y suben el bloque al centro. Lista con viñetas cian animada (b@8-10).

## Gráficos / B-roll
Iconos 3D con glow (celular, checklist, logo WhatsApp) que entran junto al presentador; números grandes ("17", "6.8 M");
B-roll de stock (mujer con celular, empresario) 3-5 s con caption encima; un inserto en blanco y negro de 1 s (b@17).

## Look (color)
- A (noche): L medio 34, contraste ×0.92 vs. tu material, casta magenta (+7.6 a), saturación alta. → `luts/peruano-A-noche.cube`
- B (día): L medio 49, contraste ×1.08, ligera casta cálida (+3 a, +1.7 b), saturación alta. → `luts/peruano-B-dia.cube`
- Ambos extraídos con `tools/lookmatch.py` (transferencia estadística en Lab, exposición propia conservada). Usar al 60-70 %.

## Audio
A: −12.5 LUFS con pico +0.1 dBTP (está clipeando, muy alto para Instagram que normaliza a −14). B: −20.7 LUFS (bajo).
Los dos llevan música de fondo bajo la voz. El nuestro va a −14.8 LUFS, correcto.

## Qué copiar y qué no
Copiar: flash a blanco en cambios de locación, captions a media altura con palabra clave grande, punch-ins, iconos con glow
cuando se nombra algo concreto (aire, envío, garantía), música de fondo suave.
No copiar: el clipping de audio del video A.
