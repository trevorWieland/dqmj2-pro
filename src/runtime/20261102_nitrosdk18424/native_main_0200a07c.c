typedef unsigned short int u16;
typedef unsigned long u32;
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
struct SNDWaveArc;
typedef struct SNDWaveArcLink {
	struct SNDWaveArc * waveArc;
	struct SNDWaveArcLink * next;
} SNDWaveArcLink;
typedef struct SNDWaveArc {
	struct SNDBinaryFileHeader fileHeader;
	struct SNDBinaryBlockHeader blockHeader;
	struct SNDWaveArcLink * topLink;
	u32 reserved[7];
	u32 waveCount;
	u32 waveOffset[0];
} SNDWaveArc;
typedef struct SNDBankData {
	struct SNDBinaryFileHeader fileHeader;
	struct SNDBinaryBlockHeader blockHeader;
	struct SNDWaveArcLink waveArcLink[4 ];
	u32 instCount;
	u32 instOffset[0];
} SNDBankData;
typedef struct SNDInstPos {
	u32 prgNo;
	u32 index;
} SNDInstPos;
struct SNDInstPos native_main_0200a07c(const struct SNDBankData * bank);
SNDInstPos native_main_0200a07c (const SNDBankData * bank)
{
    SNDInstPos pos;
    ((void) 0) ;
    (void)bank;
    pos.prgNo = 0;
    pos.index = 0;
    return pos;
}
