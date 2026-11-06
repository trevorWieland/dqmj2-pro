#include "types.h"

void native_main_02031800 (NNSG3dRS * rs, u32)
{
    ((void) 0) ;
    if (!(rs->flag & NNS_G3D_RSFLAG_OPT_SKIP_SBCDRAW) &&
        (rs->flag & NNS_G3D_RSFLAG_NODE_VISIBLE)) {
        BOOL cbFlag;
        NNSG3dSbcCallBackTiming cbTiming;
        if ((rs->pMatAnmResult->prmTexImage & 0xc0000000 ) !=
            (GX_TEXGEN_NORMAL << 30 )) {
            extern u32 native_data_main_020dd690[4];
            rs->pMatAnmResult->prmTexImage &= ~0xc0000000 ;
            rs->pMatAnmResult->prmTexImage |= GX_TEXGEN_NORMAL << 30 ;
            native_data_main_020dd690[3] = rs->pMatAnmResult->prmTexImage;
            NNS_G3dGeBufferData_N(&native_data_main_020dd690[2], 2);
        }
        NNS_G3dGeMtxMode(GX_MTXMODE_TEXTURE);
        cbFlag = NNSi_G3dCallBackCheck_A(rs, 0x0c , &cbTiming);
        if (!cbFlag) {
            s32 width, height;
            width = (s32)rs->pMatAnmResult->origWidth;
            height = (s32)rs->pMatAnmResult->origHeight;
            {
                NNS_G3dGeScale(width << (12 + 3), -height << (12 + 3), ((fx32) 0x0000000000001000L) << 4);
                NNS_G3dGeTexCoord(width << (12 - 1), height << (12 - 1));
            }
        }
        cbFlag = NNSi_G3dCallBackCheck_B(rs, 0x0c , &cbTiming);
        if (!cbFlag) {
            u32 idxMat = *(rs->c + 1);
            const NNSG3dResMatData * mat =
                NNS_G3dGetMatDataByIdx(rs->pResMat, idxMat);
            if (mat->flag & NNS_G3D_MATFLAG_EFFECTMTX) {
                const MtxFx44 * effect_mtx;
                const u8 * p = (const u8 *)mat + sizeof(NNSG3dResMatData);
                if (!(mat->flag & NNS_G3D_MATFLAG_TEXMTX_SCALEONE)) {
                    p += sizeof(fx32) + sizeof(fx32);
                }
                if (!(mat->flag & NNS_G3D_MATFLAG_TEXMTX_ROTZERO)) {
                    p += sizeof(fx16) + sizeof(fx16);
                }
                if (!(mat->flag & NNS_G3D_MATFLAG_TEXMTX_TRANSZERO)) {
                    p += sizeof(fx32) + sizeof(fx32);
                }
                effect_mtx = (const MtxFx44 *)p;
                NNS_G3dGeMultMtx44(effect_mtx);
            }
        }
        cbFlag = NNSi_G3dCallBackCheck_C(rs, 0x0c , cbTiming);
        if (!cbFlag) {
            MtxFx33 n;
            NNS_G3dGeMtxMode(GX_MTXMODE_POSITION_VECTOR);
            native_fn_02031ef0(((void *)0) , &n);
            NNS_G3dGeMtxMode(GX_MTXMODE_TEXTURE);
            if (native_data_main_020edf90.flag & NNS_G3D_GLB_FLAG_FLUSH_WVP) {
                NNS_G3dGeMultMtx33((const MtxFx33 *)NNS_G3dGlbGetCameraMtx());
                NNS_G3dGeMultMtx33(NNS_G3dGlbGetBaseRot());
                NNS_G3dGeMultMtx33(&n);
            } else if (native_data_main_020edf90.flag & NNS_G3D_GLB_FLAG_FLUSH_VP)   {
                NNS_G3dGeMultMtx33((const MtxFx33 *)NNS_G3dGlbGetCameraMtx());
                NNS_G3dGeMultMtx33(&n);
            } else {
                NNS_G3dGeMultMtx33(&n);
            }
        }
        NNS_G3dGeMtxMode(GX_MTXMODE_POSITION_VECTOR);
    }
    rs->c += 3;
}
