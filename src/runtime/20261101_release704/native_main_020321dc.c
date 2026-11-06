typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned int u32;
        typedef int BOOL;
typedef u32 NNSGfdTexKey;
typedef int (*NNSGfdFuncFreeTexVram)(NNSGfdTexKey key);
extern NNSGfdFuncFreeTexVram native_data_020dd8c4;
inline int NNS_GfdFreeTexVram (NNSGfdTexKey memKey)
{
    return (*native_data_020dd8c4)(memKey);
}
typedef u32 NNSGfdPlttKey;
typedef int (*NNSGfdFuncFreePlttVram)(NNSGfdPlttKey plttKey);
extern NNSGfdFuncFreePlttVram native_data_020dd8bc;
inline int NNS_GfdFreePlttVram (NNSGfdPlttKey plttKey)
{
    return (*native_data_020dd8bc)(plttKey);
}
typedef struct NNSG3dResFileHeader_ {
    union {
        char signature[4];
        u32 sigVal;
    };
    u16 byteOrder;
    u16 version;
    u32 fileSize;
    u16 headerSize;
    u16 dataBlocks;
} NNSG3dResFileHeader;
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
typedef struct NNSG3dResMdlSet_ {
    NNSG3dResDataBlockHeader header;
    NNSG3dResDict dict;
} NNSG3dResMdlSet;
typedef u32 NNSG3dTexKey;
typedef u32 NNSG3dPlttKey;
unsigned int native_fn_0202ed24(void *pTex, signed int *texKey, signed int *tex4x4Key);
unsigned int native_fn_0202eddc(void *pTex);
void native_fn_0202f48c(NNSG3dResMdlSet * pMdlSet);
void native_main_020321dc(void * pResData);
NNSG3dResMdlSet * native_fn_0202bedc(const NNSG3dResFileHeader * header);
unsigned int native_fn_0202beec(void *header);
void native_main_020321dc (void * pResData)
{
    u8 * binFile = (u8 *)pResData;
    BOOL failed = 0 ;
    switch (*(u32 *)&binFile[0]) {
    case '0DMB' :
    {
        NNSG3dResTex * tex;
        NNSG3dResMdlSet * mdlSet = native_fn_0202bedc(pResData);
        tex = (NNSG3dResTex *)native_fn_0202beec(pResData);
        if (tex) {
            native_fn_0202f48c(mdlSet);
        }
    }
    case '0XTB' :
    {
        NNSG3dResTex * tex;
        NNSG3dPlttKey plttKey;
        NNSG3dTexKey texKey, tex4x4Key;
        int status;
        tex = (NNSG3dResTex *)native_fn_0202beec(pResData);
        if (tex) {
            plttKey = native_fn_0202eddc(tex);
            native_fn_0202ed24(tex, (signed int *)&texKey, (signed int *)&tex4x4Key);
            if (plttKey > 0) {
                status = NNS_GfdFreePlttVram(plttKey);
            }
            if (tex4x4Key > 0) {
                status = NNS_GfdFreeTexVram(tex4x4Key);
            }
            if (texKey > 0) {
                status = NNS_GfdFreeTexVram(texKey);
            }
        }
    }
    break;
    case '0ACB' :
    case '0AVB' :
    case '0AMB' :
    case '0PTB' :
    case '0ATB' :
        break;
    default:
        break;
    };
}
