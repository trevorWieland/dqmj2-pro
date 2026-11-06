#include "context_00.h"
void native_main_0202d974 (const NNSG3dMatAnmResult * anm)
{
    struct {
        u32 cmd;
        u32 mode_tex;
        MtxFx44 m;
        u32 mode_pos_vec;
    } data;
    ((void) 0) ;
    ((void) 0)
                                ;
    if (anm->flag & NNS_G3D_MATANM_RESULTFLAG_TEXMTX_SET) {
        data.cmd = ((u32)((0x10) | (( 0x16) << 8) | (( 0x10) << 16) | (( 0x00) << 24))) ;
    } else {
        data.cmd = ((u32)((0x10) | (( 0x18) << 8) | (( 0x10) << 16) | (( 0x00) << 24))) ;
    }
    data.mode_tex = GX_MTXMODE_TEXTURE;
    data.mode_pos_vec = GX_MTXMODE_POSITION_VECTOR;
    data.m._02 = data.m._03 = data.m._12 = data.m._13 =
    data.m._20 = data.m._21 = data.m._22 = data.m._23 = data.m._32 = 0;
    data.m._33 = ((fx32) 0x0000000000001000L) ;
    {
        NNSG3dMatAnmResult * a = (NNSG3dMatAnmResult *) anm;
        if (anm->flag & NNS_G3D_MATANM_RESULTFLAG_TEXMTX_SCALEONE) {
            a->scaleS = a->scaleT = ((fx32) 0x0000000000001000L) ;
        }
        if (anm->flag & NNS_G3D_MATANM_RESULTFLAG_TEXMTX_ROTZERO) {
            a->cosR = ((fx32) 0x0000000000001000L) ;
            a->sinR = 0;
        }
        if (anm->flag & NNS_G3D_MATANM_RESULTFLAG_TEXMTX_TRANSZERO) {
            a->transS = a->transT = 0;
        }
    }
    (*native_data_main_020dd5d4.field_0000[anm->flag & (NNS_G3D_MATANM_RESULTFLAG_TEXMTX_SCALEONE |
                               NNS_G3D_MATANM_RESULTFLAG_TEXMTX_ROTZERO |
                               NNS_G3D_MATANM_RESULTFLAG_TEXMTX_TRANSZERO)])(&data.m, anm);
    if (anm->magW != ((fx32) 0x0000000000001000L) ) {
        data.m._00 = (fx32)((fx64)anm->magW * data.m._00 >> 12 );
        data.m._01 = (fx32)((fx64)anm->magW * data.m._01 >> 12 );
        data.m._30 = (fx32)((fx64)anm->magW * data.m._30 >> 12 );
    }
    if (anm->magH != ((fx32) 0x0000000000001000L) ) {
        data.m._10 = (fx32)((fx64)anm->magH * data.m._10 >> 12 );
        data.m._11 = (fx32)((fx64)anm->magH * data.m._11 >> 12 );
        data.m._31 = (fx32)((fx64)anm->magH * data.m._31 >> 12 );
    }
    NNS_G3dGeBufferData_N((u32 *)&data.cmd, sizeof(data) / 4);
}
