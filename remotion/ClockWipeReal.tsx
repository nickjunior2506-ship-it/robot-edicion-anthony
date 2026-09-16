// ClockWipeReal — adaptación de demos/transition/wipe-transitions/ClockWipe.tsx a VIDEO REAL en 9:16.
// Escena A (cola del clip anterior) debajo; escena B (cabeza del siguiente) encima con clip-path en abanico
// que gira 0→360° desde las 12 en punto. Línea de barrido con halo + borde oscuro + núcleo blanco.
// Duración: DUR fotogramas @30fps = toda la transición (sin holds, porque el resto lo pone ffmpeg).
import React from 'react';
import { AbsoluteFill, OffthreadVideo, interpolate, staticFile, useCurrentFrame } from 'remotion';

export const CW_W = 1080;
export const CW_H = 1920;
export const CW_DUR = 18; // 0.6 s

const CX = CW_W / 2;
const CY = CW_H / 2;
const R = 2400; // > distancia centro→esquina (~1101 en 1080x1920), el abanico cubre las esquinas
const SEGS = 72;

const polar = (deg: number, r: number): [number, number] => {
  const a = (deg * Math.PI) / 180;
  return [CX + r * Math.sin(a), CY - r * Math.cos(a)];
};

const fanClip = (theta: number): string => {
  const pts: string[] = [`${CX}px ${CY}px`];
  for (let i = 0; i <= SEGS; i++) {
    const [x, y] = polar((theta * i) / SEGS, R);
    pts.push(`${x.toFixed(1)}px ${y.toFixed(1)}px`);
  }
  return `polygon(${pts.join(', ')})`;
};

export type ClockWipeRealProps = { a: string; b: string };

export const ClockWipeReal: React.FC<ClockWipeRealProps> = ({ a, b }) => {
  const frame = useCurrentFrame();
  // barrido lineal (radar) en los primeros DUR-2 fotogramas; los últimos 2 = B a pantalla completa
  const theta = interpolate(frame, [0, CW_DUR - 2], [0, 360], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const wipeDone = frame >= CW_DUR - 2;
  const lineOpacity = interpolate(frame, [CW_DUR - 3, CW_DUR - 1], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const [x2, y2] = polar(theta, R);

  return (
    <AbsoluteFill style={{ background: '#000' }}>
      {!wipeDone && (
        <AbsoluteFill>
          <OffthreadVideo src={staticFile(a)} muted style={{ width: CW_W, height: CW_H, objectFit: 'cover' }} />
        </AbsoluteFill>
      )}
      <AbsoluteFill style={wipeDone ? undefined : { clipPath: fanClip(theta) }}>
        <OffthreadVideo src={staticFile(b)} muted style={{ width: CW_W, height: CW_H, objectFit: 'cover' }} />
      </AbsoluteFill>
      {!wipeDone && (
        <svg width={CW_W} height={CW_H} style={{ position: 'absolute', inset: 0, opacity: lineOpacity, pointerEvents: 'none' }}>
          <line x1={CX} y1={CY} x2={x2} y2={y2} stroke="rgba(255,255,255,0.35)" strokeWidth={26} strokeLinecap="round" />
          <line x1={CX} y1={CY} x2={x2} y2={y2} stroke="rgba(255,255,255,0.60)" strokeWidth={13} strokeLinecap="round" />
          <line x1={CX} y1={CY} x2={x2} y2={y2} stroke="rgba(0,0,0,0.55)" strokeWidth={9} strokeLinecap="round" />
          <line x1={CX} y1={CY} x2={x2} y2={y2} stroke="rgba(255,255,255,0.95)" strokeWidth={4} strokeLinecap="round" />
        </svg>
      )}
    </AbsoluteFill>
  );
};
