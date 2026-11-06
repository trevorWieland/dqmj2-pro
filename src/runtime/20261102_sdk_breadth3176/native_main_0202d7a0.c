typedef unsigned short int u16;
typedef unsigned int u32;
typedef signed short int s16;
typedef signed int s32;
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
extern const u16 (*ctrdgi_fl_maxtime);
void native_fn_02002458(fx32 numer, fx32 denom);
fx32 native_fn_020023c4(void);
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
void native_main_0202d7a0 (MtxFx44 * m, const NNSG3dMatAnmResult * anm)
{
    fx32 ss_sin, ss_cos;
    fx32 st_sin, st_cos;
    fx32 tmpW, tmpH;
    tmpW = (s32)anm->origWidth << 12 ;
    tmpH = (s32)anm->origHeight << 12 ;
    native_fn_02002458(tmpH, tmpW);
    ss_sin = (fx32)((fx64)anm->scaleS * anm->sinR >> 12 );
    ss_cos = (fx32)((fx64)anm->scaleS * anm->cosR >> 12 );
    st_sin = (fx32)((fx64)anm->scaleT * anm->sinR >> 12 );
    st_cos = (fx32)((fx64)anm->scaleT * anm->cosR >> 12 );
    m->_00 = ss_cos;
    m->_11 = st_cos;
    m->_01 = st_sin * native_fn_020023c4() >> 12 ;
    native_fn_02002458(tmpW, tmpH);
    m->_30 = (anm->origWidth * (ss_sin)) << 4;
    m->_31 = (-anm->origHeight * (st_cos - ((fx32) 0x0000000000001000L) )) << 4;
    m->_10 = -ss_sin * native_fn_020023c4() >> 12 ;
}
