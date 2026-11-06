#include "context_00.h"
void native_main_0202d5e8 (MtxFx44 * m, const NNSG3dMatAnmResult * anm)
{
    fx32 tmpW, tmpH;
    fx32 p, q;
    tmpW = (s32)anm->origWidth << 12 ;
    tmpH = (s32)anm->origHeight << 12 ;
    native_fn_02002458(tmpH, tmpW);
    m->_00 = anm->cosR;
    m->_11 = anm->cosR;
    m->_01 = anm->sinR * native_fn_020023c4() >> 12 ;
    native_fn_02002458(tmpW, tmpH);
    p = (fx32)(((fx64)anm->transS * anm->cosR + (fx64)anm->transT * anm->sinR) >> 12 );
    q = (fx32)(((fx64)anm->transS * anm->sinR - (fx64)anm->transT * anm->cosR) >> 12 );
    m->_30 = (anm->origWidth * (anm->sinR - p)) << 4;
    m->_31 = (-anm->origHeight * (anm->cosR + q - ((fx32) 0x0000000000001000L) )) << 4;
    m->_10 = -anm->sinR * native_fn_020023c4() >> 12 ;
}
