typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned int u32;
typedef signed short int s16;
typedef signed int s32;
typedef s32 fx32;
typedef s16 fx16;
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
typedef struct NNSG3dResAnmHeader_ {
    u8 category0;
    u8 revision;
    u16 category1;
} NNSG3dResAnmHeader;
typedef struct NNSG3dAnmObj_ {
    fx32 frame;
    fx32 ratio;
    void * resAnm;
    void * funcAnm;
    struct NNSG3dAnmObj_ * next;
    const NNSG3dResTex * resTex;
    u8 priority;
    u8 numMapData;
    u16 mapData[1];
} NNSG3dAnmObj;
void native_main_0202e8b8(u32 rawObject, u32 rawAnimation, s32 rawModel, u32 rawTexture);
struct NNSG3dResMdl_;
typedef void (*NNSG3dAnimInitFunc)(NNSG3dAnmObj *, void *, const NNSG3dResMdl *);
typedef struct {
    u8 category0;
    u8 dummy_;
    u16 category1;
    NNSG3dAnimInitFunc func;
} NNSG3dAnmObjInitFunc;
extern u32 native_data_020dd5f4;
extern NNSG3dAnmObjInitFunc native_data_020dd618[10 ];
void native_main_0202e8b8(u32 rawObject, u32 rawAnimation, s32 rawModel, u32 rawTexture)
{
    NNSG3dAnmObj *pAnmObj = (NNSG3dAnmObj *)rawObject;
    void *pResAnm = (void *)rawAnimation;
    const NNSG3dResMdl *pResMdl = (const NNSG3dResMdl *)(u32)rawModel;
    const NNSG3dResTex *pResTex = (const NNSG3dResTex *)rawTexture;
    const NNSG3dResAnmHeader * hdr;
    u32 i;
    pAnmObj->frame = 0;
    pAnmObj->resAnm = (void *)pResAnm;
    pAnmObj->next = ((void *)0) ;
    pAnmObj->priority = 127;
    pAnmObj->ratio = ((fx32) 0x0000000000001000L) ;
    pAnmObj->resTex = pResTex;
    pAnmObj->numMapData = 0;
    pAnmObj->funcAnm = ((void *)0) ;
    hdr = (const NNSG3dResAnmHeader *)pResAnm;
    for (i = 0; i < native_data_020dd5f4; ++i) {
        if (native_data_020dd618[i].category0 == hdr->category0 &&
            native_data_020dd618[i].category1 == hdr->category1) {
            if (native_data_020dd618[i].func) {
                (*native_data_020dd618[i].func)(pAnmObj, pResAnm, pResMdl);
            }
            break;
        }
    }
}
