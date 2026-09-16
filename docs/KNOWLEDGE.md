# 🤖 Robot de Edición — Base de Conocimiento

> Todo el aprendizaje para construir el bot que convierte video crudo en contenido pro publicable.
> Consolidado de: investigación de 40 videos de YouTube (edición viral + limpieza de audio, EN/ES,
> transcripciones reales) + specs técnicos de plataformas 2026 + el kit `ai-video-studio-kit`.
> Última actualización: 2026-08-09. Idioma de trabajo del bot: español (RD).

---

## 0. La arquitectura ganadora (lo más importante)

Los creadores que YA tienen un "editor con IA" funcionando NO dejan que la IA corte el video crudo directo (eso todavía falla: timing, cortes raros). Usan un **pipeline híbrido de 2 etapas**:

1. **Corte a nivel de TEXTO primero** (transcript de Whisper / Descript): se limpia borrando líneas del guion — muletillas, repeticiones, tomas malas. Esto es lo confiable hoy. NO delegarle al LLM la decisión de dónde cortar el metraje.
2. **IA solo como capa de POST-PRODUCCIÓN** (no de corte): con el corte ya limpio, un agente (Claude Code) aplica estilo usando reglas de marca **guardadas como archivos** (no re-prompteadas cada vez). Ahí sí brilla: motion graphics, captions con brand kit, sound effects según el audio, B-roll generado.

**Regla de oro del bot:** separar SIEMPRE (a) corte/limpieza confiable de (b) post-producción con estilo. Verificar el corte antes de gastar en la capa cara.

---

## 1. EXPORT / TÉCNICO (el export que el bot NO debe equivocar)

Un solo preset sirve para TikTok / Reels / Shorts / FB / X:

| Parámetro | Valor |
|---|---|
| Resolución | 1080 x 1920 (9:16) |
| Contenedor / codec | MP4 · H.264 **High Profile L4.2+** · audio AAC |
| FPS | 30 (60 solo si la fuente se grabó a 60) |
| Bitrate | 10–15 Mbps (<8 = artefactos · >20 = sin ganancia en móvil) |

⚠️ Nunca H.265 (uploads fallan / procesan lento).

---

## 2. AUDIO — el 50% invisible de la calidad

### Cadena de voz (voiceover) — probada, no "a ojo"
`high-pass 80Hz → cortar ~500Hz (mud) → +2–3dB en 2–5kHz (presencia) → de-ess 6–8kHz → compresión ~3:1 → limitar a −1.0 dBTP → normalizar a LUFS objetivo`

### Volumen / Loudness por destino
- **YouTube / Reels:** −14 LUFS (normalizan hacia abajo igual).
- **TikTok:** NO normaliza en feed → el más fuerte suena más fuerte. Si TikTok es el destino principal, masterizar a **−9 a −11 LUFS**.
- **Techo duro −1.0 dBTP** SIEMPRE (evita distorsión tras el re-encode de la plataforma).

### Limpieza de ruido — reglas críticas
- **Denoise SOLO en los silencios, no sobre la voz.** Cuando hay voz, ésta enmascara el ruido (efecto de máscara de frecuencias). Usar los **timestamps de Whisper**: donde no hay palabra = aplicar reducción; donde hay voz = dejar.
- Reducción: empezar en **~12 dB** (no 16). Más = voz robótica.
- **Nunca cortar el final de S / R ni las respiraciones** (suena antinatural).
- **High-pass (EQ band 1)** para viento / rumble de baja frecuencia. Se pueden apilar técnicas.
- Reducción de ruido de 2 pasos (estilo Audacity): seleccionar tramo de solo-ruido → "obtener perfil de ruido" → aplicar al resto.
- **Atajo IA:** Adobe Podcast "Enhance Speech" (gratis) para audio sucio, ANTES del pipeline. Aviso: no salva audio pésimo y puede robotizar.

### Música
- Bed **18–20 dB debajo** de la voz; duck automático bajo la voz (sidechain).
- **Silencio total de música ~2–3s en el pico emocional.** Usar el silencio una vez, fuerte. Cola de música bajando en los últimos 3–5s.

---

## 3. RITMO / CORTES

- **Ritmo por BPM (el #1 de alto impacto):** si hay música, cortar en múltiplos del beat (1 / 2 / 4 cortes por beat). Si no, dar ritmo con la locución.
- **Cortes por minuto: 20–40.** Ningún plano estático > 3s.
- **Nunca repetir la misma duración de plano 3× seguidas.** Respiración cinematográfica: `8s → 5s → 3s → 2s → 10s`.
- Eliminar pausas: cortar silencio **> 250 ms** (media respiración, aire pre-toma). Cortar en límites de palabra.
- **Zoom-in con keyframes + curvas de velocidad (ease)** — nunca movimiento lineal brusco. J-cuts / L-cuts en las 3–4 transiciones más duras.
- Los cortes deben **revelar algo nuevo** o marcar cambio de idea — no cortar por cortar (exceso = frenético, baja confianza).

---

## 4. GANCHO / RETENCIÓN (primeros 3 segundos)

- El espectador decide en **~1.7s.** Frame 1: **texto en pantalla antes de 0.5s** + voz inmediata + movimiento. Nunca abrir en beat estático/silencioso.
- **Hold rate objetivo a los 3s: ≥ 55%** (mínimo para que el algoritmo distribuya, 2026).
- **Primer subtítulo ≤ 7 palabras.** Sin disolvencias en los primeros 5s.
- El primer frame = **gancho visual** (el autoplay va sin audio).
- **Cerrar en LOOP** — el último beat conecta con el primero para replay sin costura.
- Duración: viral ~30–40s · valor ~60–90s.

---

## 5. SUBTÍTULOS / CAPTIONS

| Parámetro | Valor |
|---|---|
| Fuente | Sans-serif bold (Montserrat Bold = estándar short-form) |
| Altura | 6–9% del alto del video (≈36–48 px sobre 1080x1920) |
| Máx. por línea | ≤ 30–42 caracteres · ≤ 2 líneas |
| **ZONA SEGURA** | centro. Evitar **20% superior** (usuario/título) y **25% inferior** (botones like/comentar/compartir) → si van abajo, quedan tapados por la interfaz |
| Estilo | word-by-word: palabra activa con color + glow, pasadas se atenúan, un grupo en pantalla, hard-kill al final (no texto colgando) |
| Timing | sincronizados a timestamps de palabra (Whisper word-level); cue termina +200ms tras la última palabra |
| Contraste | stroke o caja de fondo SIEMPRE |

---

## 6. LOOK "CARO" (post-producción)

- **Hacer MENOS pero mejor** (estilo Apple): no saturar de efectos.
- **Color:** normalizar → temp → balance → curvas → eq → (LUT opcional). Intensidad 0.6–0.85. Nunca saturación >1.2 en personas. Look barato cinematográfico sin LUT: `contrast 1.06, saturate 0.88, brightness 0.92` + viñeta radial suave.
- **Transiciones:** máx. 4 tipos en toda la pieza. Prohibidos por default (se ven baratos): wipes, push/slide, zoom blur, RGB split, light leaks, glitch.
- **Sound design:** whoosh en movimientos + "tick"/switch cuando aparece un texto → percepción de pulido.
- **Rotar A-roll → B-roll → motion graphics** cada pocos segundos (cambio visual = atención).
- **Motion graphics:** mínimo 3 capas por escena; fondo nunca vacío (glows radiales, tipografía gigante atenuada, polvo de profundidad). Contraste de peso 300 vs 900 (no 400 vs 700).

---

## 7. MARCA + ESTILO (rellenar con la marca real — Facilito / Nick)

> **Capa de estilo:** ver `ESTILOS-EDICION.md` — catálogo de 6 estilos de edición que venden (presets A–F), con recomendación de prioridad para Facilito. Default = Estilo A (Minimalismo Dinámico).


### Brand kit por DEFAULT (recomendado, activo 2026-08-10 — Nick puede cambiarlo cuando dé su marca real)

- **Estilo default:** A · Minimalismo Dinámico (ver `ESTILOS-EDICION.md`). Recetas concretas en `RECETARIO-TACTICO.md`.
- **Fuentes:** Montserrat — Black (900) MAYÚSCULAS para hooks/énfasis · SemiBold (600) para cuerpo. Poppins SemiBold para precio/cuota/lower-third. Máx. 2 fuentes por pieza.
- **Colores (hex):**
  - Texto caption: `#FFFFFF` blanco + stroke negro `#000000` (4–8 px) o caja `rgba(0,0,0,0.65)`.
  - Highlight palabra activa (primario): `#2979FF` **azul confianza** (encaja con crédito/serio). Solo 1 palabra resaltada.
  - Acento precio/CTA/número: `#FFB300` **ámbar premium**.
  - Palabras pasadas: blanco 60–70% opacidad.
- **Grade base:** `contrast 1.06 · saturate 0.88 · brightness 0.92 · temp −3` + viñeta 15% + grain 2% (por estilo, ver `RECETARIO-TACTICO.md §7.1`).
- **SFX default:** tick al aparecer texto clave + 1 whoosh por cambio de escena + boom en el hook. −12/−18 dB bajo la voz.
- **Posición fija de captions:** centro vertical, dentro de zona segura (evitar 20% superior y 25% inferior — `§5`).
- **Logo / marca de agua:** arriba-derecha, ancho ≈120 px, opacidad 85%, margen 6% del borde (dentro de zona segura). ⚠️ **PENDIENTE:** Nick debe entregar el PNG del logo real; hasta entonces se produce sin marca de agua.
- **Idioma captions:** **es** (español coloquial RD).

---

## 8. QA GATE (correr antes de dar un video por terminado)

- ¿Frame 1 con texto antes de 0.5s + movimiento + voz? ¿Cambio visual cada 1–3s? ¿El loop cierra?
- ¿Ninguna duración de plano repetida 3× seguidas? ¿≤4 tipos de transición, cero efectos prohibidos?
- ¿Captions word-synced, ≤2 líneas, dentro de zona segura, hard-kill al final?
- ¿Voz pasó por la cadena + LUFS objetivo? ¿Música ducked + un silencio en el pico? ¿Techo −1 dBTP?
- ¿Export correcto (1080x1920, H.264 High, 30fps, 10–15 Mbps)?
- ¿Runtime dentro de ±10% del objetivo?

---

## 9. QUÉ CONSTRUIR EN EL BOT (roadmap de módulos)

1. **Limpieza de audio automática** — normalizar → denoise solo en silencios (usando timestamps de Whisper) → igualar a LUFS objetivo → limitar −1 dBTP. *(Aprovecha el Whisper que ya está instalado.)*
2. **Corte por transcript** — limpiar muletillas/repeticiones/pausas >250ms desde el texto, antes de clipear.
3. **Motor de ritmo** — detectar BPM de la música y alinear cortes al beat.
4. **Capa de captions** — word-by-word, zona segura, brand kit fijo.
5. **Rotación A-roll/B-roll/motion graphics** automática.
6. **Export preset** fijo + QA gate automático.

---

## Fuentes y notas
- Reglas de arte/audio base: `~/Downloads/ai-video-studio-kit/EDITING-CRAFT.md` (kit del que sale este bot; tiene el bridge a DaVinci Resolve y skills de motion/film director).
- Investigación YouTube (transcripciones reales vía yt-dlp, 2026-08-09): edición viral (Learn By Leo 5.4M, vidIQ 1M, NaughtyyJuan 926k, Diego Hernández 1.4M, Jhon Vargas, Alejandro Luengo, Milo 2.4M) + limpieza de audio (DaVinci Resolve, Primal Video, Nico Astegiano 313k, Audacity/Aural Mind, DiegoLVlogs 264k).
- Specs de plataforma 2026: LUFS (forasoft, mrvocal), captions/zona segura (OpusClip, Blitzcut, VEED), export (hevcut, clipspeed), retención (CapCut, faceless.so, aibrify).
- Memoria de contexto: `~/.claude/.../memory/ai-video-studio-kit.md`.
