/* 0x020337c4 (main, ARM, 364 B) -- NNS G3D joint-animation pivot writer.

   This is the 20261102_joint_decode364_v2 source with ONE correction: the pivot
   table is native_data_020d90ac, not native_data_020d9aac. The image's literal pool
   holds 0x020d90ac + {0,1,2,3}, i.e. row 0 of a 9x4 byte table at 0x020d90ac; the
   v2 draft named a symbol 0xA00 higher, which compiled to the right shape and the
   wrong pointer. The queue scan caught it in the relocation-only bucket (the shim
   normalizes pool words through the symbol, so a misnamed data symbol is invisible
   to duplicate/objdump diffing but not to the byte comparison).

   Verified: score (0, 0) against the module image through ops/form_search.py with
   TargetModes. See docs/authoring/permuter-queue-v2.md. */
typedef unsigned char u8;
typedef unsigned long u32;
typedef signed short int s16;
typedef signed int s32;
        typedef int BOOL;
typedef s32 fx32;
typedef s16 fx16;
    typedef union {
        struct {
            fx32 _00, _01, _02;
            fx32 _10, _11, _12;
            fx32 _20, _21, _22;
        };
        fx32 m[3][3];
        fx32 a[9];
    } MtxFx33;
typedef enum {
    NNS_G3D_JNTANM_PIVOTINFO_IDXPIVOT_MASK   = 0x000f,
    NNS_G3D_JNTANM_PIVOTINFO_MINUS           = 0x0010,
    NNS_G3D_JNTANM_PIVOTINFO_SIGN_REVC       = 0x0020,
    NNS_G3D_JNTANM_PIVOTINFO_SIGN_REVD       = 0x0040,
    NNS_G3D_JNTANM_PIVOT_INFO_IDXPIVOT_SHIFT = 0
} NNSG3dJntAnmPivotInfo;
typedef enum {
    NNS_G3D_JNTANM_RIDX_PIVOT         = 0x8000,
    NNS_G3D_JNTANM_RIDX_IDXDATA_MASK  = 0x7fff,
    NNS_G3D_JNTANM_RIDX_IDXDATA_SHIFT = 0
} NNSG3dJntAnmRIdx;
BOOL native_main_020337c4(MtxFx33 * pRot, const void * pArrayRot3, const void * pArrayRot5, NNSG3dJntAnmRIdx info);
extern const u8 native_data_020d90ac[9][4];
BOOL native_main_020337c4 (MtxFx33 * pRot, const void * pArrayRot3, const void * pArrayRot5, NNSG3dJntAnmRIdx info)
{
    if (info & NNS_G3D_JNTANM_RIDX_PIVOT) {
        const fx16 * data;
        fx32 A, B;
        u32 idxPivot;
        pRot->_00 = pRot->_01 = pRot->_02 =
        pRot->_10 = pRot->_11 = pRot->_12 =
        pRot->_20 = pRot->_21 = pRot->_22 = 0;
        data = (const fx16 *)pArrayRot3 + ((info & NNS_G3D_JNTANM_RIDX_IDXDATA_MASK) * 3);
        A = *(data + 1);
        B = *(data + 2);
        idxPivot = (u32)((*data & NNS_G3D_JNTANM_PIVOTINFO_IDXPIVOT_MASK) >>
                         NNS_G3D_JNTANM_PIVOT_INFO_IDXPIVOT_SHIFT);
        pRot->a[idxPivot] =
            (*data & NNS_G3D_JNTANM_PIVOTINFO_MINUS) ? -((fx32) 0x0000000000001000L) : ((fx32) 0x0000000000001000L) ;
        pRot->a[native_data_020d90ac[idxPivot][0]] = A;
        pRot->a[native_data_020d90ac[idxPivot][1]] = B;
        pRot->a[native_data_020d90ac[idxPivot][2]] =
            (*data & NNS_G3D_JNTANM_PIVOTINFO_SIGN_REVC) ? -B : B;
        pRot->a[native_data_020d90ac[idxPivot][3]] =
            (*data & NNS_G3D_JNTANM_PIVOTINFO_SIGN_REVD) ? -A : A;
        return 0 ;
    } else {
        const fx16 * data = (fx16 *)pArrayRot5 +
                            ((info & NNS_G3D_JNTANM_RIDX_IDXDATA_MASK) * 5);
        fx16 _12;
        _12 = (fx16)(data[4] & 7);
        pRot->_11 = (data[4] >> 3);
        _12 = (fx16)((_12 << 3) | (data[0] & 7));
        pRot->_00 = (data[0] >> 3);
        _12 = (fx16)((_12 << 3) | (data[1] & 7));
        pRot->_01 = (data[1] >> 3);
        _12 = (fx16)((_12 << 3) | (data[2] & 7));
        pRot->_02 = (data[2] >> 3);
        _12 = (fx16)((_12 << 3) | (data[3] & 7));
        pRot->_10 = (data[3] >> 3);
        pRot->_12 = ((fx16)(_12 << 3) >> 3);
        return 1 ;
    }
}

typedef char checked_u32_width[(sizeof(u32)==4)?1:-1];
