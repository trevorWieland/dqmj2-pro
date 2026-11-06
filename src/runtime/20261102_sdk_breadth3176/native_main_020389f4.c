typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned int u32;
typedef struct SNDBinaryFileHeader {
	char signature[4];
	u16 byteOrder;
	u16 version;
	u32 fileSize;
	u16 headerSize;
	u16 dataBlocks;
} SNDBinaryFileHeader;
typedef struct SNDBinaryBlockHeader {
	u32 kind;
	u32 size;
} SNDBinaryBlockHeader;
typedef struct NNSSndSeqParam {
    u16 bankNo;
    u8 volume;
    u8 channelPrio;
    u8 playerPrio;
    u8 playerNo;
    u16 reserved;
} NNSSndSeqParam;
typedef struct NNSSndSeqArcSeqInfo {
    u32 offset;
    struct NNSSndSeqParam param;
} NNSSndSeqArcSeqInfo;
typedef struct NNSSndSeqArc {
    struct SNDBinaryFileHeader fileHeader;
    struct SNDBinaryBlockHeader blockHeader;
    u32 baseOffset;
    u32 count;
    NNSSndSeqArcSeqInfo info[0];
} NNSSndSeqArc;
const NNSSndSeqArcSeqInfo * native_main_020389f4(const struct NNSSndSeqArc * seqArc, int seqNo);
const NNSSndSeqArcSeqInfo * native_main_020389f4 (const NNSSndSeqArc * seqArc, int index)
{
    ((void) 0) ;
    if (index < 0) return ((void *)0) ;
    if (index >= seqArc->count) return ((void *)0) ;
    if (seqArc->info[ index ].offset == 0xffffffff ) return ((void *)0) ;
    return &seqArc->info[ index ];
}
