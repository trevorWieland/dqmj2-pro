typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned int u32;
typedef signed short int s16;
typedef signed int s32;
typedef s32 fx32;
typedef s16 fx16;
typedef enum {
	GX_TEXFMT_NONE       = 0,
	GX_TEXFMT_A3I5       = 1,
	GX_TEXFMT_PLTT4      = 2,
	GX_TEXFMT_PLTT16     = 3,
	GX_TEXFMT_PLTT256    = 4,
	GX_TEXFMT_COMP4x4    = 5,
	GX_TEXFMT_A5I3       = 6,
	GX_TEXFMT_DIRECT     = 7
} GXTexFmt;
extern const u16 (*ctrdgi_fl_maxtime);
fx32 native_fn_0200235c(fx32 numer, fx32 denom);
typedef u32 NNSGfdTexKey;
inline u32 NNS_GfdGetTexKeyAddr (NNSGfdTexKey memKey)
{
    return (u32)(((0x0000FFFF & memKey)) << 3 );
}
typedef struct NNSG3dResDataBlockHeader_ {
    union {
        u32 kind;
        char chr[4];
    };
    u32 size;
} NNSG3dResDataBlockHeader;
typedef struct NNSG3dResDictTreeNode_ {
    u8 refBit;
    u8 idxLeft;
    u8 idxRight;
    u8 idxEntry;
} NNSG3dResDictTreeNode;
typedef struct NNSG3dResDict_ {
    u8 revision;
    u8 numEntry;
    u16 sizeDictBlk;
    u16 dummy_;
    u16 ofsEntry;
    NNSG3dResDictTreeNode node[1];
} NNSG3dResDict;
typedef union NNSG3dResName_ {
    char name[(16) ];
    u32 val[((16) / sizeof(u32)) ];
} NNSG3dResName;
typedef enum {
    NNS_G3D_TEXIMAGE_PARAMEX_ORIGW_MASK   = 0x000007ff,
    NNS_G3D_TEXIMAGE_PARAMEX_ORIGH_MASK   = 0x003ff800,
    NNS_G3D_TEXIMAGE_PARAMEX_WHSAME_MASK  = 0x80000000,
    NNS_G3D_TEXIMAGE_PARAMEX_ORIGW_SHIFT  = 0,
    NNS_G3D_TEXIMAGE_PARAMEX_ORIGH_SHIFT  = 11,
    NNS_G3D_TEXIMAGE_PARAMEX_WHSAME_SHIFT = 31
} NNSG3dTexImageParamEx;
typedef struct NNSG3dResDictTexData_ {
    u32 texImageParam;
    u32 extraParam;
} NNSG3dResDictTexData;
typedef struct NNSG3dResTexInfo_ {
    NNSGfdTexKey vramKey;
    u16 sizeTex;
    u16 ofsDict;
    u16 flag;
    u16 dummy_;
    u32 ofsTex;
} NNSG3dResTexInfo;
typedef struct NNSG3dResTex4x4Info_ {
    NNSGfdTexKey vramKey;
    u16 sizeTex;
    u16 ofsDict;
    u16 flag;
    u16 dummy_;
    u32 ofsTex;
    u32 ofsTexPlttIdx;
} NNSG3dResTex4x4Info;
typedef struct NNSG3dResPlttInfo_ {
    NNSGfdTexKey vramKey;
    u16 sizePltt;
    u16 flag;
    u16 ofsDict;
    u16 dummy_;
    u32 ofsPlttData;
} NNSG3dResPlttInfo;
typedef struct NNSG3dResTex_ {
    NNSG3dResDataBlockHeader header;
    NNSG3dResTexInfo texInfo;
    NNSG3dResTex4x4Info tex4x4Info;
    NNSG3dResPlttInfo plttInfo;
    NNSG3dResDict dict;
} NNSG3dResTex;
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
void * native_fn_0202bbb4(const NNSG3dResDict * dict, const NNSG3dResName * name);
inline NNSG3dResDictTexData * NNS_G3dGetTexDataByName(const NNSG3dResTex * tex, const NNSG3dResName * name);
inline NNSG3dResDictTexData * NNS_G3dGetTexDataByName (const NNSG3dResTex * tex, const NNSG3dResName * name)
{
    ((void) 0) ;
    if (tex)
        return (NNSG3dResDictTexData *)native_fn_0202bbb4(&tex->dict, name);
    else
        return ((void *)0) ;
}
void native_main_02034248 (const NNSG3dResTex * pTex, const NNSG3dResName * pTexName, NNSG3dMatAnmResult * pResult)
{
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0)
                      ;
    ((void) 0)
                      ;
    {
        const NNSG3dResDictTexData * pData = NNS_G3dGetTexDataByName(pTex, pTexName);
        ((void) 0) ;
        {
            const u32 vramOffset = ((pData->texImageParam & 0x1c000000 ) !=
                                    (GX_TEXFMT_COMP4x4 << 26 )) ?
                                   NNS_GfdGetTexKeyAddr(pTex->texInfo.vramKey) >> 3 :
                                   NNS_GfdGetTexKeyAddr(pTex->tex4x4Info.vramKey) >> 3 ;
            pResult->prmTexImage &= 0xc0000000 |
                                    0x00080000 | 0x00040000 |
                                    0x00020000 | 0x00010000 ;
            pResult->prmTexImage |= pData->texImageParam + vramOffset;
            pResult->origWidth = (u16)((pData->extraParam & NNS_G3D_TEXIMAGE_PARAMEX_ORIGW_MASK) >>
                                       NNS_G3D_TEXIMAGE_PARAMEX_ORIGW_SHIFT);
            pResult->origHeight = (u16)((pData->extraParam & NNS_G3D_TEXIMAGE_PARAMEX_ORIGH_MASK) >>
                                        NNS_G3D_TEXIMAGE_PARAMEX_ORIGH_SHIFT);
            {
                const s32 w = (s32)(((pData->extraParam) & NNS_G3D_TEXIMAGE_PARAMEX_ORIGW_MASK) >> NNS_G3D_TEXIMAGE_PARAMEX_ORIGW_SHIFT);
                const s32 h = (s32)(((pData->extraParam) & NNS_G3D_TEXIMAGE_PARAMEX_ORIGH_MASK) >> NNS_G3D_TEXIMAGE_PARAMEX_ORIGH_SHIFT);
                pResult->magW = (w != pResult->origWidth) ?
                                native_fn_0200235c(w << 12 , pResult->origWidth << 12 ) :
                                ((fx32) 0x0000000000001000L) ;
                pResult->magH = (h != pResult->origHeight) ?
                                native_fn_0200235c(h << 12 , pResult->origHeight << 12 ) :
                                ((fx32) 0x0000000000001000L) ;
            }
        }
    }
}
