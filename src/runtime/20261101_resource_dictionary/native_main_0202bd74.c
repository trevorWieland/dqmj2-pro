typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
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
inline const NNSG3dResName * NNS_G3dGetResNameByIdx(const NNSG3dResDict * dict, u32 idx);
unsigned int native_main_0202bd74(signed int rawDict, unsigned char *rawName);
inline const NNSG3dResName * NNS_G3dGetResNameByIdx (const NNSG3dResDict * dict, u32 idx)
{
    NNSG3dResDictEntryHeader * hdr;
    if (dict != ((void *)0) && idx < dict->numEntry) {
        hdr = (NNSG3dResDictEntryHeader *)((u8 *)dict + dict->ofsEntry);
        return (NNSG3dResName *)((u8 *)hdr +
                                 hdr->ofsName +
                                 sizeof(NNSG3dResName) * idx);
    } else {
        return ((void *)0) ;
    }
}
unsigned int native_main_0202bd74(signed int rawDict, unsigned char *rawName)
{
    const NNSG3dResDict *dict = (const NNSG3dResDict *)rawDict;
    const NNSG3dResName *name = (const NNSG3dResName *)rawName;
    if (!name)
        return -1;
    if (dict->numEntry < 16) {
        u32 idx;
        const NNSG3dResName * n;
        u32 v0 = name->val[0];
        u32 v1 = name->val[1];
        u32 v2 = name->val[2];
        u32 v3 = name->val[3];
        for (idx = 0; idx < dict->numEntry; ++idx) {
            n = NNS_G3dGetResNameByIdx(dict, idx);
            if (n->val[0] == v0 &&
                n->val[1] == v1 &&
                n->val[2] == v2 &&
                n->val[3] == v3) {
                return (int)idx;
            }
        }
    } else {
        const NNSG3dResName * n;
        const NNSG3dResDictTreeNode * treeBase;
        const NNSG3dResDictTreeNode * p, * x;
        treeBase = &dict->node[0];
        p = treeBase;
        if (p->idxLeft != 0) {
            x = treeBase + p->idxLeft;
            while (p->refBit > x->refBit) {
                p = x;
                x = treeBase + *(&x->idxLeft +
                                 ((name->val[x->refBit >> 5] >> (x->refBit & 31)) & 1));
            }
            n = NNS_G3dGetResNameByIdx(dict, x->idxEntry);
            if (n->val[0] == name->val[0] &&
                n->val[1] == name->val[1] &&
                n->val[2] == name->val[2] &&
                n->val[3] == name->val[3]) {
                return x->idxEntry;
            }
        }
    }
    return -1;
}
