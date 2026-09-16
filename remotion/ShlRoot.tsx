// ============================================================
//  Robot de Edición Anthony (REA) · v1.0.0
//  Autor:    Anthony
//  Contacto: WhatsApp +1 (849) 517-8351 · https://wa.me/18495178351
//  Repo:     https://github.com/nickjunior2506-ship-it/robot-edicion-anthony
//  Licencia: MIT (ver LICENSE). Si lo usas o modificas, conserva este crédito.
// ============================================================
// Entrada separada para las transiciones del reel SMART HOME LUXURY (no toca Root.tsx del template).
import { Composition } from 'remotion';
import { ClockWipeReal, CW_DUR, CW_W, CW_H } from './ClockWipeReal';

export const ShlRoot: React.FC = () => (
  <Composition
    id="ClockWipeReal"
    component={ClockWipeReal}
    durationInFrames={CW_DUR}
    fps={30}
    width={CW_W}
    height={CW_H}
    defaultProps={{ a: 'shl/t1a.mp4', b: 'shl/t1b.mp4' }}
  />
);
