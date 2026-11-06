#include "context_00.h"
#include "context_01.h"
void native_main_02031b44 (NNSG3dRS * rs, u32)
{
    ((void) 0) ;
    if (!(rs->flag & NNS_G3D_RSFLAG_OPT_SKIP_SBCDRAW) &&
        (rs->flag & NNS_G3D_RSFLAG_NODE_VISIBLE)) {
        BOOL cbFlag;
        NNSG3dSbcCallBackTiming cbTiming;
        MtxFx43 m;
        native_fn_main_02031ef0(&m, ((void *)0) );
        NNS_G3dGeStoreMtx((30) );
        if ((rs->pMatAnmResult->prmTexImage & 0xc0000000 ) !=
            (GX_TEXGEN_VERTEX << 30 )) {
            rs->pMatAnmResult->prmTexImage &= ~0xc0000000 ;
            rs->pMatAnmResult->prmTexImage |= GX_TEXGEN_VERTEX << 30 ;
            native_data_main_020dd690[1] = rs->pMatAnmResult->prmTexImage;
            NNS_G3dGeBufferData_N(&native_data_main_020dd690[0], 2);
        }
        cbFlag = NNSi_G3dCallBackCheck_A(rs, 0x0d , &cbTiming);
        if (!cbFlag) {
            s32 width, height;
            width = (s32)rs->pMatAnmResult->origWidth;
            height = (s32)rs->pMatAnmResult->origHeight;
            {
                native_data_main_020dd6c0._00 = width << (12 + 3);
                native_data_main_020dd6c0._11 = -height << (12 + 3);
                native_data_main_020dd6c0._30 = width << (12 + 3);
                native_data_main_020dd6c0._31 = height << (12 + 3);
                NNS_G3dGeLoadMtx44(&native_data_main_020dd6c0);
            }
        }
        cbFlag = NNSi_G3dCallBackCheck_B(rs, 0x0d , &cbTiming);
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
        cbFlag = NNSi_G3dCallBackCheck_C(rs, 0x0d , cbTiming);
        if (!cbFlag) {
            MtxFx44 tex_mtx;
            if (native_data_main_020edf90.flag & NNS_G3D_GLB_FLAG_FLUSH_WVP) {
                NNS_G3dGeTranslateVec(NNS_G3dGlbGetBaseTrans());
                NNS_G3dGeMultMtx33(NNS_G3dGlbGetBaseRot());
                NNS_G3dGeMultMtx43(&m);
            } else if (native_data_main_020edf90.flag & NNS_G3D_GLB_FLAG_FLUSH_VP)   {
                NNS_G3dGeMultMtx43(&m);
            } else {
                NNS_G3dGeMultMtx43(native_fn_main_0202e74c());
                NNS_G3dGeMultMtx43(&m);
            }
            {
                native_fn_main_0202e300();
                G3_MtxMode(GX_MTXMODE_PROJECTION);
                G3_PushMtx();
                G3_Identity();
                while (native_fn_main_02004668(&tex_mtx))
                    ;
                G3_PopMtx(1);
                G3_MtxMode(GX_MTXMODE_TEXTURE);
            }
            NNS_G3dGeLoadMtx44(&tex_mtx);
            NNS_G3dGeTexCoord(tex_mtx._30 >> 4, tex_mtx._31 >> 4);
        }
        NNS_G3dGeMtxMode(GX_MTXMODE_POSITION_VECTOR);
        NNS_G3dGeRestoreMtx((30) );
    }
    rs->c += 3;
}
