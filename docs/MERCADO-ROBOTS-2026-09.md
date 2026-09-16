# Robots de edición de video disponibles — inventario 2026-09-15

Investigación con WebFetch a páginas oficiales de pricing/docs el 2026-09-15. Etiquetas: ✅ CONFIRMADO en fuente oficial · 🟡 SUPUESTO (terceros) · ❓ no verificado.
Complementa a KNOWLEDGE.md (doctrina) y al AI Video Studio Kit (motores locales en ~/Downloads/ai-video-studio-kit).

## 1. Video largo → clips verticales
| Herramienta | Qué hace | API | Precio entrada | Precio con API | Link | Evidencia |
|---|---|---|---|---|---|---|
| Opus Clip | Detecta momentos virales, clips verticales con captions | Sí (plan Business: Video Editing API + Scheduler API + MCP) | Free / Starter $15/mes / Pro $29/mes | Business custom | opus.pro/pricing | ✅ |
| Klap | Clips verticales multi-red | Sí, precio no público | Basic $14/mes anual (100 clips) | "hablar con ventas" | klap.app/pricing | ✅ plan · 🟡 API |
| Vizard | Clipping + reframe + subtítulos + B-roll IA | Sí, rate limits 1-10 req/min según plan | Free (60 créditos) | Incluida en Creator/Business | vizard.ai/pricing | ✅ |
| Submagic | Clips + captions animados + b-roll + limpieza audio | Sí, créditos aparte | Starter $19/mes | $0.10–0.23/min | submagic.co/pricing | ✅ |
| Munch | Repurposing multi-plataforma | ❓ | ~$49/mes (agregadores) | ❓ | getmunch.com → munchstudio.com | 🟡 |

## 2. Editores generalistas (edición por texto/transcript)
| Herramienta | Qué hace | API | Precio | Link | Evidencia |
|---|---|---|---|---|---|
| Descript | Edita video/audio editando el texto; Underlord IA | Sí, API + MCP | Free / Hobbyist $16 / Creator $24 mes | descript.com/pricing | ✅ (tarifa de uso API no visible) |
| CapCut | Generalista con IA | ❓ | ❓ (pricing 404 en 2 rutas) | capcut.com | 🟡 |
| Runway | Editor + generación | Sí (dev.runway.com, créditos) | Free / Standard $12-15 / Pro $28-35 mes | runway.com/pricing | ✅ consumer · 🟡 API |
| Adobe Premiere (Firefly) | Generative Extend, object removal | Sin API pública confirmada | Creative Cloud | adobe.com | ❓ |
| Filmora | Generalista con IA | ❓ | ❓ | filmora.wondershare.com | ❓ |

## 3. Programables / open source
| Herramienta | Qué hace | API/CLI | Precio | Link | Evidencia |
|---|---|---|---|---|---|
| auto-editor | Corta silencios por loudness/movimiento; exporta a Premiere/Resolve/FCP | CLI | Gratis, Unlicense, 5.2k ⭐ | github.com/WyattBlue/auto-editor | ✅ |
| Remotion | Video programático en React | Framework | Gratis ≤3 empleados; Company: $25/seat/mes o $0.01/render (mín $100/mes) | remotion.dev/docs/license | ✅ |
| VideoDB | API para ingest/indexar/buscar/generar video | API/SDK | Free ($20 créditos) / Pro $20/mes + uso | videodb.io/pricing | ✅ |
| MoviePy | Librería Python de edición | Librería | Gratis MIT | — | 🟡 |
| FFmpeg + LLM | Patrón: LLM genera comandos ffmpeg | CLI | Gratis | ffmpeg.org | 🟡 patrón |
| Editly / Revideo | Ensamblado declarativo JS/TS | Código | Gratis OSS | github.com/mifi/editly · revideo.dev | 🟡 |

## 4. B-roll generado (API)
| Herramienta | API | Precio API | Evidencia |
|---|---|---|---|
| Google Veo 3.1 (Gemini API) | Sí | Standard $0.40/s (720-1080p), $0.60/s 4K; Fast $0.10-0.12/s; Lite $0.05-0.08/s | ✅ ai.google.dev/gemini-api/docs/pricing |
| OpenAI Sora 2 | Sí | Standard $0.10/s; Pro $0.30-0.70/s | ✅ developers.openai.com — ⚠️ un tercero menciona sunset 24-sep-2026, doc oficial no lo dice: ❓ verificar |
| Luma Ray3.2 | Sí | 5s $0.15 (540p) – $1.20 (1080p); 10s hasta $3.60 | ✅ lumalabs.ai/api |
| Kling AI | Sí | Prepago desde $9.80; ~$0.075/s (agregadores) | 🟡 |
| Runway Gen | Sí | créditos, tarifa no extraída | 🟡 |
| Pika | Sí (dev.pika.art) | Free / $8 / $28 / $76 mes; API aparte | ✅ plan · 🟡 API |

## 5. Captions y limpieza de audio
| Herramienta | Qué hace | API | Precio | Evidencia |
|---|---|---|---|---|
| Submagic | Captions animados + limpieza | Sí | $19/mes | ✅ |
| Captions.ai | Captions + AI actors + edición conversacional | No encontrada | Free / Max $24.99/mes | ✅ (móvil-first) |
| Adobe Podcast Enhance | Limpieza de voz IA | ❓ | Gratis | ✅ gratis · ❓ API |
| ElevenLabs Voice Isolator + STT | Aislar voz, transcribir, doblar | Sí | Free / Starter $6 / Creator $11 mes; isolator 1,000 créditos/min | ✅ |

## Top 5 para automatizar "crudo → clips verticales con captions"
1. Vizard — API con límites explícitos, pipeline completo en un producto.
2. Opus Clip Business — API + scheduler + MCP, se enchufa a n8n/agente; precio custom.
3. Submagic — etapa final (captions + audio) por créditos baratos, encadenable tras un clipper.
4. auto-editor + FFmpeg + Whisper + LLM — stack propio $0, control total, más ingeniería. (Ya tienes ffmpeg + whisper + el kit local.)
5. VideoDB — infraestructura API-first para un agente custom.

## ❓ Pendiente de verificar
CapCut (precio/API) · Kling (tabla oficial API) · Munch · Adobe Premiere API · Filmora/MoviePy/Editly/Revideo (no fetcheados) · Sora 2 sunset · tarifas de uso de Descript/Klap/Runway/Pika.
