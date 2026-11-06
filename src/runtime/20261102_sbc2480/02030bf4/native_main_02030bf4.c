#include "types.h"

void native_main_02030bf4 (NNSG3dRS * rs, u32 opt)
{
    u32 cmdLen = 2;
    MtxFx44 m;
    extern u32 native_data_main_020dd748[18];
    VecFx32 * trans = (VecFx32 *)&native_data_main_020dd748[12];
    VecFx32 * scale = (VecFx32 *)&native_data_main_020dd748[15];
    MtxFx43 * mtx = (MtxFx43 *)&native_data_main_020dd748[3];
    BOOL cbFlag;
    NNSG3dSbcCallBackTiming cbTiming;
    ((void) 0) ;
    if (rs->flag & NNS_G3D_RSFLAG_OPT_SKIP_SBCDRAW) {
        if (opt == 0x40 ||
            opt == 0x60 ) {
            ++cmdLen;
        }
        if (opt == 0x20 ||
            opt == 0x60 ) {
            ++cmdLen;
        }
        rs->c += cmdLen;
        return;
    }
    {
        if (opt == 0x40 ||
            opt == 0x60 ) {
            ++cmdLen;
            if (!(rs->flag & NNS_G3D_RSFLAG_OPT_NOGECMD)) {
                u32 idxMtxSrc;
                if (opt == 0x40 ) {
                    idxMtxSrc = *(rs->c + 2);
                } else {
                    idxMtxSrc = *(rs->c + 3);
                }
                ((void) 0) ;
                native_fn_0202e434(0x14 ,
                                    &idxMtxSrc,
                                    1);
            }
        }
    }
    cbFlag = NNSi_G3dCallBackCheck_A(rs, 0x08 , &cbTiming);
    if (!(rs->flag & NNS_G3D_RSFLAG_OPT_NOGECMD) &&
        (!cbFlag)) {
        native_fn_0202e300();
        (*( REGType32v *) (0x04000000 + 0x400)) = ((u32)((0x10) | (( 0x11) << 8) | (( 0x15) << 16) | (( 0x00) << 24))) ;
        (*( REGType32v *) (0x04000000 + 0x400)) = (u32)GX_MTXMODE_PROJECTION;
        (*( REGType32v *) (0x04000000 + 0x400)) = 0;
        while (native_fn_02004668(&m))
            ;
        if (native_data_main_020edf90.flag & NNS_G3D_GLB_FLAG_FLUSH_WVP) {
            const MtxFx43 * cam = NNS_G3dGlbGetSrtCameraMtx();
            MtxFx44 tmp;
            MTX_Copy43To44(cam, &tmp);
            native_fn_02001bac(&m, &tmp, &m);
        } else if (native_data_main_020edf90.flag & NNS_G3D_GLB_FLAG_FLUSH_VP)   {
            const MtxFx43 * cam = NNS_G3dGlbGetCameraMtx();
            MtxFx44 tmp;
            MTX_Copy43To44(cam, &tmp);
            native_fn_02001bac(&m, &tmp, &m);
        }
        trans->x = m._30;
        trans->y = m._31;
        trans->z = m._32;
        scale->x = native_fn_020025b8((VecFx32 *)&m._00);
        scale->y = native_fn_020025b8((VecFx32 *)&m._10);
        scale->z = native_fn_020025b8((VecFx32 *)&m._20);
        if (m._11 != 0 || m._12 != 0) {
            native_fn_02002618((VecFx32 *)&m._10, (VecFx32 *)&mtx->_10);
            mtx->_21 = -mtx->_12;
            mtx->_22 = mtx->_11;
        } else {
            native_fn_02002618((VecFx32 *)&m._20, (VecFx32 *)&mtx->_20);
            mtx->_12 = -mtx->_21;
            mtx->_11 = mtx->_22;
        }
        if (native_data_main_020edf90.flag & NNS_G3D_GLB_FLAG_FLUSH_WVP) {
            (*( REGType32v *) (0x04000000 + 0x400)) = ((u32)((0x12) | (( 0x10) << 8) | (( 0x17) << 16) | (( 0x00) << 24))) ;
            MI_CpuSend32(&native_data_main_020dd748[1],
                         &(*( REGType32v *) (0x04000000 + 0x400)) ,
                         2 * sizeof(u32));
            MI_CpuSend32(NNS_G3dGlbGetInvSrtCameraMtx(),
                         &(*( REGType32v *) (0x04000000 + 0x400)) ,
                         12 * sizeof(u32));
            (*( REGType32v *) (0x04000000 + 0x400)) = ((u32)((0x19) | (( 0x1b) << 8) | (( 0x00) << 16) | (( 0x00) << 24))) ;
            MI_CpuSend32(&native_data_main_020dd748[3],
                         &(*( REGType32v *) (0x04000000 + 0x400)) ,
                         sizeof(MtxFx43) + sizeof(VecFx32));
        } else if (native_data_main_020edf90.flag & NNS_G3D_GLB_FLAG_FLUSH_VP)   {
            (*( REGType32v *) (0x04000000 + 0x400)) = ((u32)((0x12) | (( 0x10) << 8) | (( 0x17) << 16) | (( 0x00) << 24))) ;
            MI_CpuSend32(&native_data_main_020dd748[1],
                         &(*( REGType32v *) (0x04000000 + 0x400)) ,
                         2 * sizeof(u32));
            MI_CpuSend32(NNS_G3dGlbGetInvCameraMtx(),
                         &(*( REGType32v *) (0x04000000 + 0x400)) ,
                         12 * sizeof(u32));
            (*( REGType32v *) (0x04000000 + 0x400)) = ((u32)((0x19) | (( 0x1b) << 8) | (( 0x00) << 16) | (( 0x00) << 24))) ;
            MI_CpuSend32(&native_data_main_020dd748[3],
                         &(*( REGType32v *) (0x04000000 + 0x400)) ,
                         sizeof(MtxFx43) + sizeof(VecFx32));
        } else {
            MI_CpuSend32(&native_data_main_020dd748[0], &(*( REGType32v *) (0x04000000 + 0x400)) , 18 * sizeof(u32));
        }
    }
    cbFlag = NNSi_G3dCallBackCheck_C(rs, 0x08 , cbTiming);
    if (opt == 0x20 ||
        opt == 0x60 ) {
        ++cmdLen;
        if (!cbFlag) {
            if (!(rs->flag & NNS_G3D_RSFLAG_OPT_NOGECMD)) {
                u32 idxMtxDest;
                idxMtxDest = *(rs->c + 2);
                ((void) 0) ;
                native_fn_0202e434(0x13 ,
                                    &idxMtxDest,
                                    1 );
            }
        }
    }
    rs->c += cmdLen;
}
