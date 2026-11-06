typedef unsigned int u32;
typedef signed int s32;
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
struct NNSG3dJntAnmResult_;
typedef enum {
    NNS_G3D_JNTANM_RESULTFLAG_SCALE_ONE    = 0x00000001,
    NNS_G3D_JNTANM_RESULTFLAG_ROT_ZERO     = 0x00000002,
    NNS_G3D_JNTANM_RESULTFLAG_TRANS_ZERO   = 0x00000004,
    NNS_G3D_JNTANM_RESULTFLAG_SCALEEX0_ONE = 0x00000008,
    NNS_G3D_JNTANM_RESULTFLAG_SCALEEX1_ONE = 0x00000010,
    NNS_G3D_JNTANM_RESULTFLAG_MAYA_SSC     = 0x00000020
} NNSG3dJntAnmResultFlag;
typedef struct NNSG3dJntAnmResult_ {
    NNSG3dJntAnmResultFlag flag;
    VecFx32 scale;
    VecFx32 scaleEx0;
    VecFx32 scaleEx1;
    MtxFx33 rot;
    VecFx32 trans;
} NNSG3dJntAnmResult;
void native_main_0202c6cc(const NNSG3dJntAnmResult * result);
void native_fn_0202e434(u32 op, const u32 * args, u32 num);
void native_main_0202c6cc (const NNSG3dJntAnmResult * result)
{
    if (!(result->flag & NNS_G3D_JNTANM_RESULTFLAG_TRANS_ZERO)) {
        if (!(result->flag & NNS_G3D_JNTANM_RESULTFLAG_ROT_ZERO)) {
            native_fn_0202e434(0x19 ,
                                (u32 *)&result->rot._00,
                                12 );
        } else {
            native_fn_0202e434(0x1c ,
                                (u32 *)&result->trans.x,
                                3 );
        }
    } else {
        if (!(result->flag & NNS_G3D_JNTANM_RESULTFLAG_ROT_ZERO)) {
            native_fn_0202e434(0x1a ,
                                (u32 *)&result->rot._00,
                                9 );
        }
    }
    if (!(result->flag & NNS_G3D_JNTANM_RESULTFLAG_SCALE_ONE)) {
        native_fn_0202e434(0x1b ,
                            (u32 *)&result->scale.x,
                            3 );
    }
}
