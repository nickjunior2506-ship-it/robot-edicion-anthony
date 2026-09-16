# 🧰 Recetario Táctico — fuentes, colores, transiciones, SFX y motion

> El "toolbox" concreto que el robot aplica LITERALMENTE. `ESTILOS-EDICION.md` dice QUÉ estilo;
> este archivo dice con QUÉ elementos exactos se construye (valores reales: hex, px, ms, nombres de SFX).
> Se apoya en `KNOWLEDGE.md` (§5 captions, §6 look caro). Basado en specs short-form 2026.
> Creado: 2026-08-10. ⚠️ Los colores/fuente de MARCA de Facilito están como recomendación — Nick debe confirmarlos (ver §6).

---

## 1. FUENTES (exactas, con peso y uso)

| Uso | Fuente | Peso | Notas |
|---|---|---|---|
| **Caption principal (hook/énfasis)** | **Montserrat** | Black (900) o ExtraBold (800) | MAYÚSCULAS. Estándar short-form. Limpia = premium. |
| Caption cuerpo (frases largas) | Montserrat | SemiBold (600) | Mejor legibilidad en bloques de 2 líneas. |
| Lower-third / nombre / precio | **Poppins** | SemiBold (600) | Redondeada, moderna, se lee chiquita. |
| Números / cuota / oferta | Montserrat | Black (900) | El número SIEMPRE más grande y bold que el texto. |
| Alternativa "premium/serio" | Inter o Proxima Nova | Bold | Si se quiere look más corporativo (crédito/banca). |

**Reglas de tipografía:**
- Contraste de peso: mezclar 300 (fino atenuado de fondo) vs 900 (activo). NUNCA 400 vs 700 (se ve débil).
- Tamaño caption: 6–9% del alto (≈36–48 px sobre 1080×1920) — ya en `KNOWLEDGE.md §5`.
- Stroke negro 4–8 px O caja de fondo SIEMPRE (contraste sobre cualquier video).
- Máx. 2 fuentes por pieza. Más = amateur.

---

## 2. COLORES (hex concretos)

**Captions — base universal:**
- Texto: `#FFFFFF` blanco puro
- Stroke/sombra: `#000000` negro (grosor 4–8 px) o caja `rgba(0,0,0,0.65)`
- Palabra activa (highlight): **el color de marca** (ver §6). Solo UNA palabra resaltada a la vez.
- Palabras ya pasadas: blanco atenuado al 60–70% opacidad.

**Paletas de highlight recomendadas (elegir UNA, según marca):**
| Nombre | Hex | Sensación |
|---|---|---|
| Amarillo Hormozi | `#FFD400` | Alto contraste — PERO saturado, todo el mundo lo usa. Evitar si se puede. |
| Verde éxito | `#00E676` | "Aprobado", positivo — encaja con financiamiento OK. |
| Cian eléctrico | `#00E5FF` | Moderno, tech, juvenil. |
| Ámbar premium | `#FFB300` | Cálido, confiable, menos quemado que el amarillo. |
| Azul confianza | `#2979FF` | Serio, bancario, credibilidad (bueno para crédito). |

**Look "caro" (color grade) — ya probado en `KNOWLEDGE.md §6`:**
- `contrast 1.06 · saturate 0.88 · brightness 0.92`
- Viñeta radial suave (oscurecer bordes ~15%).
- Grain sutil (2–4%). Intensidad de grade 0.6–0.85. Nunca saturación >1.2 en personas.

---

## 3. TRANSICIONES (por nombre — cuáles SÍ y cuáles NO)

**Duración de toda transición con movimiento: 0.2–0.4s.** Más largo = se siente lento/barato.

**✅ PERMITIDAS (se ven caras):**
| Transición | Cuándo usarla |
|---|---|
| **Corte seco (hard cut)** | El 85–90% de los cortes. El default. |
| **J-cut** (audio del siguiente clip entra antes) | Transiciones suaves entre ideas. |
| **L-cut** (audio del clip actual sigue sobre el siguiente) | Diálogo/voz continua sobre B-roll. |
| **Punch-in zoom cut** (corta a un plano más cercano) | Énfasis en una palabra/idea clave. |
| **Whip pan** (paneo rápido + motion blur) | MÁX 1–2 por pieza, en cambio de escena fuerte. Lleva whoosh. |
| **Match cut** (mismo encuadre/forma → revela otra cosa) | Reveals ("el carro"). |
| **Speed-ramp cut** (acelera y corta en el beat) | Antes de un reveal o value moment. |

**⛔ PROHIBIDAS (gritan "barato"):**
Wipes, push/slide, spin/giro, page turn, star wipe, glitch, RGB split, light leaks, zoom blur genérico en cada corte, cube 3D, dissolve en los primeros 5s.
→ Regla: **máx. 4 tipos de transición en toda la pieza** (`KNOWLEDGE.md §6`).

---

## 4. EFECTOS DE AUDIO / SFX (por nombre + cuándo + nivel)

**Regla madre:** editar la MÚSICA primero, luego calzar el video al audio. Un SFX fuera de beat se ve como error, no como estilo.

| SFX | Cuándo dispararlo |
|---|---|
| **Whoosh / swoosh** | Whip pans, y cuando un texto/caption entra volando. |
| **Impact / boom (grave)** | En el hook (primer segundo) y en reveals fuertes. |
| **Tick / click / pop** | Cuando aparece un texto o número clave (percepción de pulido). |
| **Riser (subida)** | 1–2s ANTES de un reveal — crea anticipación. |
| **Bass drop / sub hit** | En el "drop" del beat de la música. |
| **Cash / ka-ching** | Al mostrar precio/cuota/oferta (opcional, sin abusar). |

**Niveles (no deben tapar la voz):**
- Voz = referencia (LUFS objetivo de `KNOWLEDGE.md §2`).
- SFX: **−12 a −18 dB** por debajo de la voz.
- Música: bed 18–20 dB debajo, con duck automático bajo la voz.
- 1 silencio total de música (2–3s) en el pico emocional.
- Techo −1.0 dBTP SIEMPRE.
- **No más de ~1 SFX cada 2–3s.** Sobrecargar = ansioso/barato.

---

## 5. EFECTOS DE VIDEO / MOTION (con settings concretos)

| Efecto | Ajuste concreto | Cuándo |
|---|---|---|
| **Punch-in zoom** | scale 100% → 108–115% en 0.3–0.5s, ease-in-out (nunca lineal) | En cada cambio de idea / énfasis. |
| **Text pop-in** | scale 80%→100% + opacity 0→100 en 0.15–0.20s, con overshoot (ease-out-back / spring) | Entrada de cada caption clave. |
| **Word highlight** | color de marca + glow suave en la palabra activa; las demás −30% opacidad | Caption word-by-word. |
| **Camera shake** | 2–4 px, 3–5 frames | Solo sincronizado con impact/boom. |
| **Speed ramp** | 100% → 300–400% (ramp up) y vuelta a 100% en el value moment | Antes de un reveal / before-after. |
| **Motion blur** | ligero, automático | En cualquier movimiento rápido (whip, ramp). |
| **Vignette + grain** | viñeta 15%, grain 2–4% | Look caro, toda la pieza. |
| **Rotación A-roll → B-roll → motion** | cambio visual cada 1–3s | Retención (`KNOWLEDGE.md §6`). |

**⛔ Motion prohibido:** chromatic aberration / RGB split constante, glitch, shake excesivo, zoom blur en cada corte, textos rotando 3D, flashes epilépticos. Todo eso se ve barato en 2026.

**Motion graphics de fondo (`KNOWLEDGE.md §6`):** mínimo 3 capas por escena; fondo nunca vacío (glows radiales, tipografía gigante atenuada al 10–15%, polvo/profundidad).

---

## 6. LO QUE FALTA DE MARCA (Nick debe confirmar — bloquea el preset final)

Para cerrar el "brand kit" del robot necesito de ti 3 cosas:
1. **Color primario de Facilito** (hex) + 1 acento. → define el highlight de captions (§2).
2. **Fuente de marca** (si tienen una) o si uso Montserrat/Poppins como default.
3. **Logo / marca de agua** (PNG) y su posición fija (dentro de zona segura, `KNOWLEDGE.md §5`).

Con eso lleno la sección 7 de `KNOWLEDGE.md` y los presets quedan listos para producir.

---

## 7. Mapa estilo → toolbox (qué usa cada estilo de `ESTILOS-EDICION.md`)

| Estilo | Fuente | Transiciones | SFX | Motion clave | Grading de color |
|---|---|---|---|---|---|
| **A. Minimalismo Dinámico** ⭐ | Montserrat 900, 2 colores | Corte seco + J/L-cut | Solo tick + 1 whoosh | Punch-in sutil, word highlight | Limpio/plano premium (frío suave) |
| **B. Talking-Head** | Montserrat 900 | Corte seco agresivo (borra pausas) | Whoosh + boom en hook | Punch-in en énfasis | Cálido favorecedor de piel |
| **C. UGC/Testimonial** | Montserrat SemiBold (simple) | Corte seco crudo | Casi nada (autenticidad) | Mínimo motion — que se sienta real | Natural "de teléfono", casi sin grade |
| **D. Faceless/Showcase** | Montserrat 900 + Poppins precio | Whip pan + match cut al beat | Whoosh + bass drop + ka-ching | Speed ramp, rotación planos | Comercial punchy (metal frío, brillo alto) |
| **E. Micro-storytelling** | según estilo base | según base | riser antes del CTA | text pop-in en cada beat narrativo | Narrativo: problema frío → solución cálido |
| **F. Showcase rápido** | Poppins precio | Speed-ramp cut al beat | Impact por corte + bass drop | Punch-in + motion blur, loop | Cinematográfico (teal&orange + viñeta fuerte) |

### 7.1 Grading de color por estilo (valores concretos)

> Todos parten del look base de `KNOWLEDGE.md §6`. Aquí el ajuste específico por estilo.
> `temp` = temperatura (+ cálido / − frío). `sat` = saturación. `con` = contraste. `bri` = brillo.

| Estilo | con | sat | bri | temp | Viñeta / Grain | Highlight caption | Sensación |
|---|---|---|---|---|---|---|---|
| **A. Minimalismo Dinámico** ⭐ | 1.06 | 0.85 | 0.95 | −3 (frío suave) | viñeta 12% · grain 2% | `#2979FF` azul confianza (mono, 1 color) | Premium, limpio, "Apple". Serio = crédito. |
| **B. Talking-Head** | 1.05 | 0.92 | 0.98 | +5 (cálido) | viñeta 15% · grain 2% · **proteger piel (sat piel ≤1.0)** | color de marca | Cara favorecida, cercano, confiable. |
| **C. UGC/Testimonial** | 1.00 | 1.00 | 1.00 | 0 (neutro) | SIN viñeta · SIN grain | blanco o color marca simple | Crudo real, "grabado con el teléfono". La NO-corrección es el estilo. |
| **D. Faceless/Showcase carros** | 1.12 | 1.10 | 1.02 | −4 (frío, realza metal) | viñeta 18% · grain 3% | `#FFB300` ámbar o color marca | Comercial punchy, la carrocería brilla. |
| **E. Micro-storytelling** | base ±, dinámico | baja en "problema", sube en "solución" | — | frío en el dolor → cálido en la solución | según segmento | según estilo base | El color cuenta la historia (frío→cálido). |
| **F. Showcase rápido premium** | 1.15 | 1.05 | 0.95 | split-tone: sombras −6 frío / luces +6 cálido | viñeta 22% · grain 4% | `#FFB300` ámbar | Cine: teal&orange suave, dramático, 1 carro estrella. |

**Reglas duras del grading (aplican a todos):**
- Nunca `sat` > 1.2 sobre personas (piel naranja = barato).
- Intensidad global del grade 0.6–0.85 (no aplastar).
- Orden del pipeline de color: normalizar → temp → balance → curvas → EQ → (LUT opcional al final).
- El grade va DESPUÉS del corte, en la etapa 2 (post), nunca sobre el crudo antes de verificar el corte.

---

## Fuentes
- Efectos virales 2026 (0.2–0.4s, punch-in, speed ramp): [InsideEditors](https://insideeditors.com/instagram-video-editing-effects/) · [Medium/CapCut](https://medium.com/@msimoliunas/the-best-capcut-effects-for-viral-videos-that-actually-keep-people-watching-7cc7aa23ef79) · [OlafMotion](https://olafmotion.com/trends-inspiration/best-youtube-editing-styles-2026/)
- Speed ramp / editar audio primero: [ARWriterAI](https://arwriterai.com/en/blog/best-capcut-effects-transitions-boost-views-2026/) · [VMEditor](https://vmeditor.in/speed-ramp-capcut-template/)
- Fuentes para video: [Descript](https://www.descript.com/blog/article/choosing-the-best-fonts-for-video-the-importance-of-typography)
- Base técnica: `KNOWLEDGE.md` + `ESTILOS-EDICION.md` (este repo).
