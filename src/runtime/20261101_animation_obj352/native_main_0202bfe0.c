typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned int u32;
typedef signed short int s16;
typedef signed int s32;
typedef s32 fx32;
typedef s16 fx16;
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
typedef struct NNSG3dResAnmHeader_ {
    u8 category0;
    u8 revision;
    u16 category1;
} NNSG3dResAnmHeader;
typedef struct NNSG3dResTexPatAnmFV_ {
    u16 idxFrame;
    u8 idTex;
    u8 idPltt;
} NNSG3dResTexPatAnmFV;
typedef struct NNSG3dResDictTexPatAnmData_ {
    u16 numFV;
    u16 flag;
    fx16 ratioDataFrame;
    u16 offset;
} NNSG3dResDictTexPatAnmData;
typedef struct NNSG3dResTexPatAnm_ {
    NNSG3dResAnmHeader anmHeader;
    u16 numFrame;
    u8 numTex;
    u8 numPltt;
    u16 ofsTexName;
    u16 ofsPlttName;
    NNSG3dResDict dict;
} NNSG3dResTexPatAnm;
const NNSG3dResTexPatAnmFV * native_main_0202bfe0(const NNSG3dResTexPatAnm * pPatAnm, u32 idx, u32 frame);
const NNSG3dResDictTexPatAnmData * native_fn_0202c054(const NNSG3dResTexPatAnm * pPatAnm, u32 idx);
inline void * NNS_G3dGetResDataByIdx(const NNSG3dResDict * dict, u32 idx);
inline void * NNS_G3dGetResDataByIdx (const NNSG3dResDict * dict, u32 idx)
{
    NNSG3dResDictEntryHeader * hdr;
    if (dict != ((void *)0) && idx < dict->numEntry) {
        hdr = (NNSG3dResDictEntryHeader *)((u8 *)dict + dict->ofsEntry);
        return (void *)(&hdr->data[0] + hdr->sizeUnit * idx);
    } else {
        return ((void *)0) ;
    }
}
const NNSG3dResTexPatAnmFV * native_main_0202bfe0 (const NNSG3dResTexPatAnm * pPatAnm, u32 idx, u32 frame)
{
    {
        const NNSG3dResDictTexPatAnmData * pAnmData =
            native_fn_0202c054(pPatAnm, idx);
        {
            const NNSG3dResTexPatAnmFV * pfvArray
                = (const NNSG3dResTexPatAnmFV *)((u8 *)pPatAnm + pAnmData->offset);
            const u32 fvIdx = (u32)((fx32)pAnmData->ratioDataFrame * frame >> 12 );
            {
                u32 realFvIdx = fvIdx;
                while (realFvIdx > 0 && pfvArray[ realFvIdx ].idxFrame >= frame) {
                    realFvIdx--;
                }
                while (realFvIdx + 1 < pAnmData->numFV && pfvArray[ realFvIdx + 1 ].idxFrame <= frame) {
                    realFvIdx++;
                }
                return &pfvArray[realFvIdx];
            }
        }
    }
}
