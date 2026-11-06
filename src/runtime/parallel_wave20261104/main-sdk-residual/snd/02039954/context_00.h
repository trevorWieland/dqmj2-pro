typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef int BOOL;
struct SNDBankData;
struct SNDBankData;
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
typedef enum SNDInstType {
	SND_INST_INVALID = 0,
	SND_INST_PCM = 0x01,
	SND_INST_PSG,
	SND_INST_NOISE,
	SND_INST_DIRECTPCM,
	SND_INST_NULL,
	SND_INST_DRUM_SET = 0x10,
	SND_INST_KEY_SPLIT
} SNDInstType;
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
typedef struct SNDInstParam {
	u16 wave[2];
	u8 original_key;
	u8 attack;
	u8 decay;
	u8 sustain;
	u8 release;
	u8 pan;
} SNDInstParam;
typedef struct SNDInstData {
	u8 type;
	u8 padding_;
	struct SNDInstParam param;
} SNDInstData;
typedef struct SNDInstPos {
	u32 prgNo;
	u32 index;
} SNDInstPos;
struct SNDInstPos native_fn_0200a07c(const struct SNDBankData * bank);
BOOL native_fn_0200a09c(const struct SNDBankData * bank, struct SNDInstData * inst, struct SNDInstPos * pos);
struct SNDBankData;
struct NNSSndHeap;
typedef struct NNSSndHeap * NNSSndHeapHandle;
struct SNDBankData;
struct SNDWaveArc;
BOOL native_main_02039954(SNDWaveArc * waveArc, const SNDBankData * bank, int waveArcNo, u32 fileId, NNSSndHeapHandle heap);
BOOL native_fn_0203988c(SNDWaveArc * waveArc, int waveNo, u32 fileId, NNSSndHeapHandle heap);
BOOL native_fn_0203988c (SNDWaveArc * waveArc, int waveNo, u32 fileId, NNSSndHeapHandle heap);
