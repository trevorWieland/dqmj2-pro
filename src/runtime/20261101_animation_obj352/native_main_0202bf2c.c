typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned int u32;
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
typedef struct NNSG3dResDictEntryHeader_ {
    u16 sizeUnit;
    u16 ofsName;
    u8 data[4];
} NNSG3dResDictEntryHeader;
typedef struct {
    u32 offset;
} NNSG3dResDictAnmSetData;
typedef struct {
    NNSG3dResDataBlockHeader header;
    NNSG3dResDict dict;
} NNSG3dResAnmSet;
u32 native_main_0202bf2c(signed int rawResource, u32 idx);
inline void * NNS_G3dGetResDataByIdx(const NNSG3dResDict * dict, u32 idx);
inline void * NNS_G3dGetResDataByIdx (const NNSG3dResDict * dict, u32 idx)
{
    NNSG3dResDictEntryHeader * hdr;
    if (dict != ((void *)0) && idx < dict->numEntry) {
        hdr = (NNSG3dResDictEntryHeader *)((u8 *)dict + dict->ofsEntry);
        return (void *)(&hdr->data[0] + hdr->sizeUnit * idx);
    } else {
        return 0;
    }
}
u32 native_main_0202bf2c (signed int rawResource, u32 idx)
{
    const void *pRes = (const void *)rawResource;
    if (pRes) {
        const NNSG3dResFileHeader * header;
        const NNSG3dResAnmSet * anmSet;
        const NNSG3dResDictAnmSetData * anmSetData;
        u32 * blks;
        header = (const NNSG3dResFileHeader *) pRes;
        blks = (u32 *)((u8 *)header + header->headerSize);
        anmSet = (const NNSG3dResAnmSet *)((u8 *)header + blks[0]);
        anmSetData = (const NNSG3dResDictAnmSetData *)NNS_G3dGetResDataByIdx(&anmSet->dict, idx);
        if (anmSetData) {
            return (u32)((u8 *)anmSet + anmSetData->offset);
        }
    }
    return 0;
}
