typedef unsigned short int u16;
typedef unsigned int u32;
typedef struct NNSG2dBinaryFileHeader {
    u32 signature;
    u16 byteOrder;
    u16 version;
    u32 fileSize;
    u16 headerSize;
    u16 dataBlocks;
} NNSG2dBinaryFileHeader;
typedef struct NNSG2dBinaryBlockHeader {
    u32 kind;
    u32 size;
} NNSG2dBinaryBlockHeader;
 u32 native_main_02034480(u32 rawHeader, u32 signature);
u32 native_main_02034480 (u32 rawHeader, u32 signature)
{
    NNSG2dBinaryFileHeader *pBinFileHeader = (NNSG2dBinaryFileHeader *)rawHeader;
    {
        NNSG2dBinaryBlockHeader * pCursor = (NNSG2dBinaryBlockHeader *)((u32)pBinFileHeader + (u32)pBinFileHeader->headerSize);
        u16 count = 0;
        while (count < pBinFileHeader->dataBlocks) {
            if (pCursor->kind == signature) {
                return (u32)pCursor;
            }
            pCursor = (NNSG2dBinaryBlockHeader *)((u32)pCursor + pCursor->size);
            count++;
        }
    }
    return 0;
}
