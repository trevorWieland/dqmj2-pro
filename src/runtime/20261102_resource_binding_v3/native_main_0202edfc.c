typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned int u32;
typedef signed int s32;
typedef s32 fx32;
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
typedef u16 NNSG3dItemTag;
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
typedef struct NNSG3dResDictEntryHeader_ {
    u16 sizeUnit;
    u16 ofsName;
    u8 data[4];
} NNSG3dResDictEntryHeader;
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
typedef struct NNSG3dResDictMatData_ {
    u32 offset;
} NNSG3dResDictMatData;
typedef struct NNSG3dResDictTexToMatIdxData_ {
    u16 offset;
    u8 numIdx;
    u8 flag;
} NNSG3dResDictTexToMatIdxData;
typedef struct NNSG3dResMatData_ {
    NNSG3dItemTag itemTag;
    u16 size;
    u32 diffAmb;
    u32 specEmi;
    u32 polyAttr;
    u32 polyAttrMask;
    u32 texImageParam;
    u32 texImageParamMask;
    u16 texPlttBase;
    u16 flag;
    u16 origWidth, origHeight;
    fx32 magW;
    fx32 magH;
} NNSG3dResMatData;
typedef struct NNSG3dResMat_ {
    u16 ofsDictTexToMatList;
    u16 ofsDictPlttToMatList;
    NNSG3dResDict dict;
} NNSG3dResMat;
inline void * NNS_G3dGetResDataByIdx(const NNSG3dResDict * dict, u32 idx);
inline NNSG3dResMatData * NNS_G3dGetMatDataByIdx(const NNSG3dResMat * mat, u32 idx);
inline void * NNS_G3dGetResDataByIdx (const NNSG3dResDict * dict, u32 idx)
{
    NNSG3dResDictEntryHeader * hdr;
    ((void) 0) ;
    if (dict != ((void *)0) && idx < dict->numEntry) {
        ((void) 0) ;
        hdr = (NNSG3dResDictEntryHeader *)((u8 *)dict + dict->ofsEntry);
        return (void *)(&hdr->data[0] + hdr->sizeUnit * idx);
    } else {
        return ((void *)0) ;
    }
}
inline NNSG3dResMatData * NNS_G3dGetMatDataByIdx (const NNSG3dResMat * mat, u32 idx)
{
    NNSG3dResDictMatData * data;
    ((void) 0) ;
    if (mat) {
        data = (NNSG3dResDictMatData *)NNS_G3dGetResDataByIdx(&mat->dict, idx);
        if (data) {
            ((void) 0) ;
            return (NNSG3dResMatData *)((u8 *)mat + data->offset);
        }
    }
    return ((void *)0) ;
}
void native_main_0202edfc (NNSG3dResMat * pMat, NNSG3dResDictTexToMatIdxData * pBindData, const NNSG3dResTex * pTex, const NNSG3dResDictTexData * pTexData)
{
    u8 * base = (u8 *)pMat + pBindData->offset;
    u32 vramOffset;
    u32 j;
    ((void) 0)                      ;
    ((void) 0)
                      ;
    if ((pTexData->texImageParam & 0x1c000000 ) !=
        (GX_TEXFMT_COMP4x4 << 26 )) {
        vramOffset = NNS_GfdGetTexKeyAddr(pTex->texInfo.vramKey) >> 3 ;
    } else {
        vramOffset = NNS_GfdGetTexKeyAddr(pTex->tex4x4Info.vramKey) >> 3 ;
    }
    for (j = 0; j < pBindData->numIdx; ++j) {
        s32 w, h;
        NNSG3dResMatData * matData = NNS_G3dGetMatDataByIdx(pMat, *(base + j));
        matData->texImageParam |= (pTexData->texImageParam + vramOffset);
        w = (s32)(((pTexData->extraParam) & NNS_G3D_TEXIMAGE_PARAMEX_ORIGW_MASK) >> NNS_G3D_TEXIMAGE_PARAMEX_ORIGW_SHIFT);
        h = (s32)(((pTexData->extraParam) & NNS_G3D_TEXIMAGE_PARAMEX_ORIGH_MASK) >> NNS_G3D_TEXIMAGE_PARAMEX_ORIGH_SHIFT);
        matData->magW = (w != matData->origWidth) ?
                        native_fn_0200235c(w << 12 , matData->origWidth << 12 ) :
                        ((fx32) 0x0000000000001000L) ;
        matData->magH = (h != matData->origHeight) ?
                        native_fn_0200235c(h << 12 , matData->origHeight << 12 ) :
                        ((fx32) 0x0000000000001000L) ;
    }
    pBindData->flag |= 1;
}
