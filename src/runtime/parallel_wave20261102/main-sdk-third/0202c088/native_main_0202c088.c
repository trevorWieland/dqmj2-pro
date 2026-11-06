#include "context_00.h"
void native_main_0202c088 (MtxFx44 * m, const NNSG3dMatAnmResult * anm)
{
    fx32 p, q;
    fx32 ss_sin, ss_cos, st_sin, st_cos;
    fx32 tmpW, tmpH;
    tmpW = (s32)anm->origWidth << 12 ;
    tmpH = (s32)anm->origHeight << 12 ;
    native_fn_02002458(tmpH, tmpW);
    ss_cos = (fx32)((fx64)anm->scaleS * anm->cosR >> 12 );
    ss_sin = (fx32)((fx64)anm->scaleS * anm->sinR >> 12 );
    st_cos = (fx32)((fx64)anm->scaleT * anm->cosR >> 12 );
    st_sin = (fx32)((fx64)anm->scaleT * anm->sinR >> 12 );
    m->_00 = ss_cos;
    m->_11 = st_cos;
    m->_01 = st_sin * native_fn_020023c4() >> 12 ;
    native_fn_02002458(tmpW, tmpH);
    p = (-anm->origWidth << (12 - 1)) - anm->transS * anm->origWidth;
    q = (-anm->origHeight << (12 - 1)) + anm->transT * anm->origHeight;
    m->_30 = (fx32)(((fx64)ss_cos * p - (fx64)ss_sin * q) >> (12 - 4)) +
             (anm->origWidth << (12 - 1 + 4));
    m->_31 = (fx32)(((fx64)st_sin * p + (fx64)st_cos * q) >> (12 - 4)) +
             (anm->origHeight << (12 - 1 + 4));
    m->_10 = -ss_sin * native_fn_020023c4() >> 12 ;
}
