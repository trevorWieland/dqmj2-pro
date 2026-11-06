#include "context_00.h"
void native_main_0202c438 (MtxFx44 * m, const NNSG3dMatAnmResult * anm)
{
    fx32 p, q;
    fx32 tmpW, tmpH;
    tmpW = (s32)anm->origWidth << 12 ;
    tmpH = (s32)anm->origHeight << 12 ;
    native_fn_02002458(tmpH, tmpW);
    m->_00 = anm->cosR;
    m->_11 = anm->cosR;
    m->_01 = anm->sinR * native_fn_020023c4() >> 12 ;
    native_fn_02002458(tmpW, tmpH);
    p = (-anm->origWidth << (12 - 1));
    q = (-anm->origHeight << (12 - 1));
    m->_30 = (fx32)(((fx64)anm->cosR * p - (fx64)anm->sinR * q) >> (12 - 4)) +
             (anm->origWidth << (12 - 1 + 4));
    m->_31 = (fx32)(((fx64)anm->sinR * p + (fx64)anm->cosR * q) >> (12 - 4)) +
             (anm->origHeight << (12 - 1 + 4));
    m->_10 = -anm->sinR * native_fn_020023c4() >> 12 ;
}
