typedef unsigned char u8;
typedef unsigned short u16;
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
typedef struct NNSG3dResMdlSet_ NNSG3dResMdlSet;

NNSG3dResMdlSet *native_main_0202bedc(const NNSG3dResFileHeader *header) {
    const u32 *blocks = (const u32 *)((const u8 *)header + header->headerSize);
    return (NNSG3dResMdlSet *)((const u8 *)header + blocks[0]);
}
