typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned int u32;
typedef signed short int s16;
typedef signed int s32;
typedef s32 fx32;
typedef s16 fx16;
extern const u16 (*ctrdgi_fl_maxtime);
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
typedef struct NNSG3dResDictTexToMatIdxData_ {
    u16 offset;
    u8 numIdx;
    u8 flag;
} NNSG3dResDictTexToMatIdxData;
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
void native_main_0202f0e4(NNSG3dResMdl * pMdl);
struct NNSG3dResMdl_;
inline void * NNS_G3dGetResDataByIdx(const NNSG3dResDict * dict, u32 idx);
inline NNSG3dResMat * NNS_G3dGetMat(const NNSG3dResMdl * mdl);
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
void native_fn_0202ef2c (NNSG3dResMat * pMat, NNSG3dResDictTexToMatIdxData * pData);
void native_main_0202f0e4 (NNSG3dResMdl * pMdl)
{
    NNSG3dResMat * mat;
    NNSG3dResDict * dictTex;
    u32 i;
    ((void) 0) ;
    mat = NNS_G3dGetMat(pMdl);
    dictTex = (NNSG3dResDict *)((u8 *)mat + mat->ofsDictTexToMatList);
    for (i = 0; i < dictTex->numEntry; ++i) {
        NNSG3dResDictTexToMatIdxData * data =
            (NNSG3dResDictTexToMatIdxData *) NNS_G3dGetResDataByIdx(dictTex, i);
        if (data->flag & 1) {
            native_fn_0202ef2c(mat, data);
        }
    }
}
