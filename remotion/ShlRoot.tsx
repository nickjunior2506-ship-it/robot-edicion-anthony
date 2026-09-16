// ============================================================
//  Robot de Edición Anthony (REA) · v1.0.1
//  Autor:    Anthony Junior Susaña Ramírez
//  Contacto: WhatsApp +1 (849) 517-8351 · https://wa.me/18495178351
//  Repo:     https://github.com/nickjunior2506-ship-it/robot-edicion-anthony
//  Licencia: USO NO COMERCIAL (ver LICENSE). Uso comercial solo con permiso
//            escrito de Anthony Junior Susaña Ramírez. Conserva este crédito.
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
