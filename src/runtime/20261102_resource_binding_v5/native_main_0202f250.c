typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned int u32;
typedef signed short int s16;
typedef signed int s32;
        typedef int BOOL;
typedef s32 fx32;
typedef s16 fx16;
extern const u16 (*ctrdgi_fl_maxtime);
typedef u32 NNSGfdTexKey;
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
typedef struct NNSG3dResDictEntryHeader_ {
    u16 sizeUnit;
    u16 ofsName;
    u8 data[4];
} NNSG3dResDictEntryHeader;
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
typedef struct NNSG3dResDictPlttData_ {
    u16 offset;
    u16 flag;
} NNSG3dResDictPlttData;
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
typedef struct NNSG3dResDictPlttToMatIdxData_ {
    u16 offset;
    u8 numIdx;
    u8 flag;
} NNSG3dResDictPlttToMatIdxData;
typedef struct NNSG3dResMat_ {
    u16 ofsDictTexToMatList;
    u16 ofsDictPlttToMatList;
    NNSG3dResDict dict;
} NNSG3dResMat;
typedef struct NNSG3dResMdlInfo_ {
    u8 sbcType;
    u8 scalingRule;
    u8 texMtxMode;
    u8 numNode;
    u8 numMat;
    u8 numShp;
    u8 firstUnusedMtxStackID;
    u8 dummy_;
    fx32 posScale;
    fx32 invPosScale;
    u16 numVertex;
    u16 numPolygon;
    u16 numTriangle;
    u16 numQuad;
    fx16 boxX, boxY, boxZ;
    fx16 boxW, boxH, boxD;
    fx32 boxPosScale;
    fx32 boxInvPosScale;
} NNSG3dResMdlInfo;
typedef struct NNSG3dResNodeInfo_ {
    NNSG3dResDict dict;
} NNSG3dResNodeInfo;
typedef struct NNSG3dResMdl_ {
    u32 size;
    u32 ofsSbc;
    u32 ofsMat;
    u32 ofsShp;
    u32 ofsEvpMtx;
    NNSG3dResMdlInfo info;
    NNSG3dResNodeInfo nodeInfo;
} NNSG3dResMdl;
BOOL native_main_0202f250(NNSG3dResMdl * pMdl, const NNSG3dResTex * pTex);
struct NNSG3dResMdl_;
inline const NNSG3dResName * NNS_G3dGetResNameByIdx(const NNSG3dResDict * dict, u32 idx);
inline void * NNS_G3dGetResDataByIdx(const NNSG3dResDict * dict, u32 idx);
extern void *native_fn_0202bbb4(const NNSG3dResDict *, const NNSG3dResName *);
inline NNSG3dResMat * NNS_G3dGetMat(const NNSG3dResMdl * mdl);
inline NNSG3dResDictPlttData * NNS_G3dGetPlttDataByName(const NNSG3dResTex * tex, const NNSG3dResName * name);
inline const NNSG3dResName * NNS_G3dGetResNameByIdx (const NNSG3dResDict * dict, u32 idx)
{
    NNSG3dResDictEntryHeader * hdr;
    ((void) 0) ;
    if (dict != ((void *)0) && idx < dict->numEntry) {
        ((void) 0) ;
        hdr = (NNSG3dResDictEntryHeader *)((u8 *)dict + dict->ofsEntry);
        return (NNSG3dResName *)((u8 *)hdr +
                                 hdr->ofsName +
                                 sizeof(NNSG3dResName) * idx);
    } else {
        return ((void *)0) ;
    }
}
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
inline NNSG3dResMat * NNS_G3dGetMat (const NNSG3dResMdl * mdl)
{
    ((void) 0) ;
    ((void) 0) ;
    if (mdl && mdl->ofsMat != 0)
        return (NNSG3dResMat *)((u8 *)mdl + mdl->ofsMat);
    else
        return ((void *)0) ;
}
inline NNSG3dResDictPlttData * NNS_G3dGetPlttDataByName (const NNSG3dResTex * tex, const NNSG3dResName * name)
{
    NNSG3dResDict * dict;
    ((void) 0) ;
    ((void) 0) ;
    if (tex && tex->plttInfo.ofsDict != 0) {
        dict = (NNSG3dResDict *)((u8 *)tex + tex->plttInfo.ofsDict);
        return (NNSG3dResDictPlttData *)native_fn_0202bbb4(dict, name);
    } else {
        return ((void *)0) ;
    }
}
void native_fn_0202f170 (NNSG3dResMat * pMat, NNSG3dResDictPlttToMatIdxData * pBindData, const NNSG3dResTex * pTex, const NNSG3dResDictPlttData * pPlttData);
BOOL native_main_0202f250 (NNSG3dResMdl * pMdl, const NNSG3dResTex * pTex)
{
    NNSG3dResMat * mat;
    NNSG3dResDict * dictPltt;
    u32 i;
    BOOL result = 1 ;
    ((void) 0) ;
    ((void) 0) ;
    mat = NNS_G3dGetMat(pMdl);
    dictPltt = (NNSG3dResDict *)((u8 *)mat + mat->ofsDictPlttToMatList);
    for (i = 0; i < dictPltt->numEntry; ++i) {
        const NNSG3dResName * name = NNS_G3dGetResNameByIdx(dictPltt, i);
        const NNSG3dResDictPlttData * plttData = NNS_G3dGetPlttDataByName(pTex, name);
        if (plttData) {
            NNSG3dResDictPlttToMatIdxData * data;
            data = (NNSG3dResDictPlttToMatIdxData *) NNS_G3dGetResDataByIdx(dictPltt, i);
            if (!(data->flag & 1)) {
                native_fn_0202f170(mat, data, pTex, plttData);
            }
        } else {
            result = 0 ;
        }
    }
    return result;
}
