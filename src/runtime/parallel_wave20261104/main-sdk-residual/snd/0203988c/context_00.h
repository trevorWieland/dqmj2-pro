typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed long s32;
typedef int BOOL;
void native_fn_020072ec(const void * startAddr, u32 nBytes);
typedef struct SNDWaveParam {
        u8 format;
        u8 loopflag;
        u16 rate;
        u16 timer;
        u16 loopstart;
        u32 looplen;
    } SNDWaveParam;
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
typedef struct SNDWaveData {
	struct SNDWaveParam param;
	u8 samples[0];
} SNDWaveData;
u32 native_fn_0200a24c(const struct SNDWaveArc * waveArc);
void native_fn_0200a254(struct SNDWaveArc * waveArc, int index, const SNDWaveData * address);
const SNDWaveData * native_fn_0200a288(const struct SNDWaveArc * waveArc, int index);
struct NNSSndHeap;
typedef void (*NNSSndHeapDisposeCallback)(void * mem, u32 size, u32 data1, u32 data2);
typedef struct NNSSndHeap * NNSSndHeapHandle;
void * native_fn_02037b94(NNSSndHeapHandle heap, u32 size, NNSSndHeapDisposeCallback callback, u32 data1, u32 data2);
struct SNDWaveArc;
s32 native_fn_02039094(u32 fileId, void * buffer, s32 size, s32 offset);
BOOL native_main_0203988c(SNDWaveArc * waveArc, int waveNo, u32 fileId, NNSSndHeapHandle heap);
void native_fn_02039844(void * mem, u32 size, u32 data1, u32 data2);
void native_fn_02039844 (void * mem, u32 size, u32 data1, u32 data2);
