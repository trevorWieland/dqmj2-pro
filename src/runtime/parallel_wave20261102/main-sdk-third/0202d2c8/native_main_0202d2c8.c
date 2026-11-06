#include "context_00.h"
void native_main_0202d2c8 (const NNSG3dMatAnmResult * anm)
{
    struct {
        u32 cmd;
        u32 mode_tex;
        MtxFx43 m;
        u32 mode_pos_vec;
    } data;
    ((void) 0) ;
    ((void) 0)
                                ;
    if (anm->flag & NNS_G3D_MATANM_RESULTFLAG_TEXMTX_SET) {
        data.cmd = ((u32)((0x10) | (( 0x17) << 8) | (( 0x10) << 16) | (( 0x00) << 24))) ;
    } else {
        data.cmd = ((u32)((0x10) | (( 0x19) << 8) | (( 0x10) << 16) | (( 0x00) << 24))) ;
    }
    data.mode_tex = GX_MTXMODE_TEXTURE;
    data.mode_pos_vec = GX_MTXMODE_POSITION_VECTOR;
    data.m._01 = data.m._02 = data.m._10 = data.m._12 = data.m._20 =
    data.m._21 = data.m._22 = data.m._32 = 0;
    if (anm->flag & NNS_G3D_MATANM_RESULTFLAG_TEXMTX_TRANSZERO) {
        data.m._30 = 0;
        data.m._31 = 0;
        if (anm->flag & NNS_G3D_MATANM_RESULTFLAG_TEXMTX_SCALEONE) {
            data.m._00 = ((fx32) 0x0000000000001000L) ;
            data.m._11 = ((fx32) 0x0000000000001000L) ;
        } else {
            data.m._00 = anm->scaleS;
            data.m._11 = anm->scaleT;
        }
    } else if (anm->flag & NNS_G3D_MATANM_RESULTFLAG_TEXMTX_SCALEONE)   {
        data.m._30 = -(anm->transS << 4) * anm->origWidth;
        data.m._31 = -(anm->transT << 4) * anm->origHeight;
        data.m._00 = ((fx32) 0x0000000000001000L) ;
        data.m._11 = ((fx32) 0x0000000000001000L) ;
    } else {
        data.m._30 = -(fx32)((fx64)anm->scaleS * anm->transS >> (12 - 4)) * anm->origWidth;
        data.m._31 = -(fx32)((fx64)anm->scaleT * anm->transT >> (12 - 4)) * anm->origHeight;
        data.m._00 = anm->scaleS;
        data.m._11 = anm->scaleT;
    }
    if (anm->magW != ((fx32) 0x0000000000001000L) ) {
        data.m._00 = (fx32)((fx64)anm->magW * data.m._00 >> 12 );
        data.m._30 = (fx32)((fx64)anm->magW * data.m._30 >> 12 );
    }
    if (anm->magH != ((fx32) 0x0000000000001000L) ) {
        data.m._11 = (fx32)((fx64)anm->magH * data.m._11 >> 12 );
        data.m._31 = (fx32)((fx64)anm->magH * data.m._31 >> 12 );
    }
    NNS_G3dGeBufferData_N((u32 *)&data.cmd, sizeof(data) / 4);
}
