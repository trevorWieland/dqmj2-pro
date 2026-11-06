typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned int u32;
typedef signed int s32;
        typedef int BOOL;
typedef s32 fx32;
typedef struct {
    fx32 x;
    fx32 y;
    fx32 z;
} VecFx32;
    typedef union {
        struct {
            fx32 _00, _01, _02;
            fx32 _10, _11, _12;
            fx32 _20, _21, _22;
        };
        fx32 m[3][3];
        fx32 a[9];
    } MtxFx33;
    static s32 FX_Whole(fx32 v);
    static inline s32 FX_Whole (fx32 v)
    {
        return (s32)(v >> 12 );
    }
extern const u16 (*ctrdgi_fl_maxtime);
void native_fn_02002618(const VecFx32 * pSrc, VecFx32 * pDst);
typedef struct NNSG3dResAnmHeader_ {
    u8 category0;
    u8 revision;
    u16 category1;
} NNSG3dResAnmHeader;
typedef enum {
    NNS_G3D_JNTANM_RINFO_STEP_1            = 0x00000000,
    NNS_G3D_JNTANM_RINFO_STEP_2            = 0x40000000,
    NNS_G3D_JNTANM_RINFO_STEP_4            = 0x80000000,
    NNS_G3D_JNTANM_RINFO_LAST_INTERP_MASK  = 0x1fff0000,
    NNS_G3D_JNTANM_RINFO_STEP_MASK         = 0xc0000000,
    NNS_G3D_JNTANM_RINFO_LAST_INTERP_SHIFT = 16,
    NNS_G3D_JNTANM_RINFO_STEP_SHIFT        = 30
} NNSG3dJntAnmRInfo;
typedef enum {
    NNS_G3D_JNTANM_RIDX_PIVOT         = 0x8000,
    NNS_G3D_JNTANM_RIDX_IDXDATA_MASK  = 0x7fff,
    NNS_G3D_JNTANM_RIDX_IDXDATA_SHIFT = 0
} NNSG3dJntAnmRIdx;
typedef enum {
    NNS_G3D_JNTANM_OPTION_INTERPOLATION = 0x01,
    NNS_G3D_JNTANM_OPTION_END_TO_START_INTERPOLATION = 0x02
} NNSG3dJntAnmOption;
typedef struct NNSG3dResJntAnm_ {
    NNSG3dResAnmHeader anmHeader;
    u16 numFrame;
    u16 numNode;
    u32 flag;
    u32 ofsRot3;
    u32 ofsRot5;
} NNSG3dResJntAnm;
void native_main_02033480(MtxFx33 * pRot, fx32 Frame, const u32 * pData, const NNSG3dResJntAnm * pJntAnm);
static BOOL native_fn_020337c4(MtxFx33 * pRot, const void * pArrayRot3, const void * pArrayRot5, NNSG3dJntAnmRIdx info);
static inline void vecCross_ (const VecFx32 * a, const VecFx32 * b, VecFx32 * axb)
{
    fx32 x, y, z;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    x = (a->y * b->z - a->z * b->y) >> 12 ;
    y = (a->z * b->x - a->x * b->z) >> 12 ;
    z = (a->x * b->y - a->y * b->x) >> 12 ;
    axb->x = x;
    axb->y = y;
    axb->z = z;
}
void native_main_02033480 (MtxFx33 * pRot, fx32 Frame, const u32 * pData, const NNSG3dResJntAnm * pJntAnm)
{
    const void * pArray = (const void *)((const u8 *)pJntAnm + *(pData + 1));
    const void * pArrayRot3 = (const void *)((const u8 *)pJntAnm + pJntAnm->ofsRot3);
    const void * pArrayRot5 = (const void *)((const u8 *)pJntAnm + pJntAnm->ofsRot5);
    NNSG3dJntAnmRInfo info = (NNSG3dJntAnmRInfo) * pData;
    u32 last_interp;
    u32 idx0, idx1;
    fx32 remainder;
    int step;
    u32 step_shift;
    u32 frame;
    const u16 * p = (const u16 *)pArray;
    frame = (u32)FX_Whole(Frame);
    if (frame == pJntAnm->numFrame - 1) {
        if (!(info & NNS_G3D_JNTANM_RINFO_STEP_MASK)) {
            idx0 = frame;
        } else if (info & NNS_G3D_JNTANM_RINFO_STEP_2)   {
            idx0 = (frame >> 1) + (frame & 1);
        } else {
            idx0 = (frame >> 2) + (frame & 3);
        }
        if (pJntAnm->flag & NNS_G3D_JNTANM_OPTION_END_TO_START_INTERPOLATION) {
            idx1 = 0;
            goto ROT_EX_0_1;
        } else {
            if (native_fn_020337c4(pRot,
                                 pArrayRot3,
                                 pArrayRot5,
                                 (NNSG3dJntAnmRIdx)p[idx0])) {
                vecCross_((const VecFx32 *)&pRot->_00,
                          (const VecFx32 *)&pRot->_10,
                          (VecFx32 *)&pRot->_20);
            } else {
                native_fn_02002618((VecFx32 *)(&pRot->_20), (VecFx32 *)(&pRot->_20));
            }
            return;
        }
    }
    if (!(info & NNS_G3D_JNTANM_RINFO_STEP_MASK)) {
        goto ROT_EX_0;
    }
    last_interp = ((u32)info & NNS_G3D_JNTANM_RINFO_LAST_INTERP_MASK) >>
                  NNS_G3D_JNTANM_RINFO_LAST_INTERP_SHIFT;
    if (info & NNS_G3D_JNTANM_RINFO_STEP_2) {
        if (frame >= last_interp) {
            idx0 = (last_interp >> 1);
            idx1 = idx0 + 1;
            goto ROT_EX_0_1;
        } else {
            idx0 = frame >> 1;
            idx1 = idx0 + 1;
            remainder = Frame & (((fx32) 0x0000000000001000L) * 2 - 1);
            step = 2;
            step_shift = 1;
            goto ROT_EX;
        }
    } else {
        if (frame >= last_interp) {
            idx0 = (frame >> 2) + (frame & 3);
            idx1 = idx0 + 1;
            goto ROT_EX_0_1;
        } else {
            idx0 = frame >> 2;
            idx1 = idx0 + 1;
            remainder = Frame & (((fx32) 0x0000000000001000L) * 4 - 1);
            step = 4;
            step_shift = 2;
            goto ROT_EX;
        }
    }
    ((void) 0) ;
ROT_EX_0:
    idx0 = (u32)frame;
    idx1 = idx0 + 1;
ROT_EX_0_1:
    remainder = Frame & (((fx32) 0x0000000000001000L) - 1);
    step = 1;
    step_shift = 0;
ROT_EX:
    {
        MtxFx33 r0, r1;
        BOOL doCross = 0 ;
        doCross |= native_fn_020337c4(&r0,
                                    pArrayRot3,
                                    pArrayRot5,
                                    (NNSG3dJntAnmRIdx)p[idx0]);
        doCross |= native_fn_020337c4(&r1,
                                    pArrayRot3,
                                    pArrayRot5,
                                    (NNSG3dJntAnmRIdx)p[idx1]);
        pRot->_00 = ((r0._00 * step) + (((r1._00 - r0._00) * remainder) >> 12 )) >> (step_shift * 0 );
        pRot->_01 = ((r0._01 * step) + (((r1._01 - r0._01) * remainder) >> 12 )) >> (step_shift * 0 );
        pRot->_02 = ((r0._02 * step) + (((r1._02 - r0._02) * remainder) >> 12 )) >> (step_shift * 0 );
        pRot->_10 = ((r0._10 * step) + (((r1._10 - r0._10) * remainder) >> 12 )) >> (step_shift * 0 );
        pRot->_11 = ((r0._11 * step) + (((r1._11 - r0._11) * remainder) >> 12 )) >> (step_shift * 0 );
        pRot->_12 = ((r0._12 * step) + (((r1._12 - r0._12) * remainder) >> 12 )) >> (step_shift * 0 );
        native_fn_02002618((VecFx32 *)(&pRot->_00), (VecFx32 *)(&pRot->_00));
        native_fn_02002618((VecFx32 *)(&pRot->_10), (VecFx32 *)(&pRot->_10));
        if (!doCross) {
            pRot->_20 = ((r0._20 * step) + (((r1._20 - r0._20) * remainder) >> 12 )) >> (step_shift * 0 );
            pRot->_21 = ((r0._21 * step) + (((r1._21 - r0._21) * remainder) >> 12 )) >> (step_shift * 0 );
            pRot->_22 = ((r0._22 * step) + (((r1._22 - r0._22) * remainder) >> 12 )) >> (step_shift * 0 );
            native_fn_02002618((VecFx32 *)(&pRot->_20), (VecFx32 *)(&pRot->_20));
        } else {
            vecCross_((const VecFx32 *)&pRot->_00,
                      (const VecFx32 *)&pRot->_10,
                      (VecFx32 *)&pRot->_20);
        }
        return;
    }
}
BOOL native_fn_020337c4 (MtxFx33 * pRot, const void * pArrayRot3, const void * pArrayRot5, NNSG3dJntAnmRIdx info);
