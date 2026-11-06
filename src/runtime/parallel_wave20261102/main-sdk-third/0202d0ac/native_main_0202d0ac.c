#include "context_00.h"
void native_main_0202d0ac (NNSG3dJntAnmResult * pResult, const fx32 * p, const u8 * cmd, u32 srtflag)
{
    u32 nodeID;
    u32 parentID;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    nodeID = *(cmd + 1);
    parentID = *(cmd + 2);
    if (srtflag & NNS_G3D_SRTFLAG_SCALE_ONE) {
        pResult->flag |= NNS_G3D_JNTANM_RESULTFLAG_SCALE_ONE;
        if (NNSi_G3dBitVecCheck(&native_data_main_020ee1f4->isScaleCacheOne[0], parentID)) {
            NNSi_G3dBitVecSet(&native_data_main_020ee1f4->isScaleCacheOne[0], nodeID);
            pResult->flag |= (NNS_G3D_JNTANM_RESULTFLAG_SCALEEX0_ONE |
                              NNS_G3D_JNTANM_RESULTFLAG_SCALEEX1_ONE);
        } else {
            MI_CpuCopy32(&native_data_main_020ee1f8.scaleCache[parentID],
                         &native_data_main_020ee1f8.scaleCache[nodeID],
                         sizeof(VecFx32) + sizeof(VecFx32));
            MI_CpuCopy32(&native_data_main_020ee1f8.scaleCache[parentID],
                         &pResult->scaleEx0,
                         sizeof(VecFx32) + sizeof(VecFx32));
        }
    } else {
        pResult->scale.x = *(p + 0);
        pResult->scale.y = *(p + 1);
        pResult->scale.z = *(p + 2);
        if (NNSi_G3dBitVecCheck(&native_data_main_020ee1f4->isScaleCacheOne[0], parentID)) {
            MI_CpuCopy32(p,
                         &native_data_main_020ee1f8.scaleCache[nodeID],
                         sizeof(VecFx32) + sizeof(VecFx32));
            NNSi_G3dBitVecReset(&native_data_main_020ee1f4->isScaleCacheOne[0], nodeID);
            pResult->flag |= (NNS_G3D_JNTANM_RESULTFLAG_SCALEEX0_ONE |
                              NNS_G3D_JNTANM_RESULTFLAG_SCALEEX1_ONE);
        } else {
            NNSi_G3dBitVecReset(&native_data_main_020ee1f4->isScaleCacheOne[0], nodeID);
            native_data_main_020ee1f8.scaleCache[nodeID].s.x =
                (fx32)((fx64)(*(p + 0)) * native_data_main_020ee1f8.scaleCache[parentID].s.x >> 12 );
            native_data_main_020ee1f8.scaleCache[nodeID].s.y =
                (fx32)((fx64)(*(p + 1)) * native_data_main_020ee1f8.scaleCache[parentID].s.y >> 12 );
            native_data_main_020ee1f8.scaleCache[nodeID].s.z =
                (fx32)((fx64)(*(p + 2)) * native_data_main_020ee1f8.scaleCache[parentID].s.z >> 12 );
            native_data_main_020ee1f8.scaleCache[nodeID].inv.x =
                (fx32)((fx64)(*(p + 3)) * native_data_main_020ee1f8.scaleCache[parentID].inv.x >> 12 );
            native_data_main_020ee1f8.scaleCache[nodeID].inv.y =
                (fx32)((fx64)(*(p + 4)) * native_data_main_020ee1f8.scaleCache[parentID].inv.y >> 12 );
            native_data_main_020ee1f8.scaleCache[nodeID].inv.z =
                (fx32)((fx64)(*(p + 5)) * native_data_main_020ee1f8.scaleCache[parentID].inv.z >> 12 );
            MI_CpuCopy32(&native_data_main_020ee1f8.scaleCache[parentID],
                         &pResult->scaleEx0,
                         sizeof(VecFx32) + sizeof(VecFx32));
        }
    }
}
