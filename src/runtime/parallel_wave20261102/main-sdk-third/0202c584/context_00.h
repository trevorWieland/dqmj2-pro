typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed short int s16;
typedef signed long s32;
typedef signed long long int s64;
typedef s32 fx32;
typedef s64 fx64;
typedef s16 fx16;
typedef union {
        struct {
            fx32 _00, _01, _02, _03;
            fx32 _10, _11, _12, _13;
            fx32 _20, _21, _22, _23;
            fx32 _30, _31, _32, _33;
        };
        fx32 m[4][4];
        fx32 a[16];
    } MtxFx44;
typedef enum {
	GX_MTXMODE_PROJECTION      = 0,
	GX_MTXMODE_POSITION        = 1,
	GX_MTXMODE_POSITION_VECTOR = 2,
	GX_MTXMODE_TEXTURE         = 3
} GXMtxMode;
extern const u16 (*ctrdgi_fl_maxtime);
struct NNSG3dMatAnmResult_;
typedef enum {
    NNS_G3D_MATANM_RESULTFLAG_TEXMTX_SCALEONE  = 0x00000001,
    NNS_G3D_MATANM_RESULTFLAG_TEXMTX_ROTZERO   = 0x00000002,
    NNS_G3D_MATANM_RESULTFLAG_TEXMTX_TRANSZERO = 0x00000004,
    NNS_G3D_MATANM_RESULTFLAG_TEXMTX_SET       = 0x00000008,
    NNS_G3D_MATANM_RESULTFLAG_TEXMTX_MULT      = 0x00000010,
    NNS_G3D_MATANM_RESULTFLAG_WIREFRAME        = 0x00000020}
NNSG3dMatAnmResultFlag;
typedef struct NNSG3dMatAnmResult_ {
    NNSG3dMatAnmResultFlag flag;
    u32 prmMatColor0;
    u32 prmMatColor1;
    u32 prmPolygonAttr;
    u32 prmTexImage;
    u32 prmTexPltt;
    fx32 scaleS, scaleT;
    fx16 sinR, cosR;
    fx32 transS, transT;
    u16 origWidth, origHeight;
    fx32 magW, magH;
} NNSG3dMatAnmResult;
void native_main_0202c584(const NNSG3dMatAnmResult * anm);
inline void NNS_G3dGeBufferData_N(const u32 * args, u32 num);
void native_fn_0202e434(u32 op, const u32 * args, u32 num);
typedef struct {
void
(*field_0000[8])(MtxFx44 *, const NNSG3dMatAnmResult *);
} NativeStorage_020dd594;
extern NativeStorage_020dd594 native_data_main_020dd594;
inline void NNS_G3dGeBufferData_N (const u32 * args, u32 num)
{
    ((void) 0) ;
    native_fn_0202e434(*args, args + 1, num - 1);
}
