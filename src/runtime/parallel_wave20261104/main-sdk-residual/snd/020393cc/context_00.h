typedef unsigned short int u16;
typedef unsigned long u32;
typedef int BOOL;
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
struct NNSSndHeap;
typedef struct NNSSndHeap * NNSSndHeapHandle;
struct SNDWaveArc;
typedef enum NNSSndArcLoadResult {
    NNS_SND_ARC_LOAD_SUCESS = 0,
    NNS_SND_ARC_LOAD_ERROR_INVALID_GROUP_NO,
    NNS_SND_ARC_LOAD_ERROR_INVALID_SEQ_NO,
    NNS_SND_ARC_LOAD_ERROR_INVALID_SEQARC_NO,
    NNS_SND_ARC_LOAD_ERROR_INVALID_BANK_NO,
    NNS_SND_ARC_LOAD_ERROR_INVALID_WAVEARC_NO,
    NNS_SND_ARC_LOAD_ERROR_FAILED_LOAD_SEQ,
    NNS_SND_ARC_LOAD_ERROR_FAILED_LOAD_SEQARC,
    NNS_SND_ARC_LOAD_ERROR_FAILED_LOAD_BANK,
    NNS_SND_ARC_LOAD_ERROR_FAILED_LOAD_WAVE
} NNSSndArcLoadResult;
NNSSndArcLoadResult native_main_020393cc(int waveArcNo, u32 loadFlag, NNSSndHeapHandle heap, BOOL bSetAddr, struct SNDWaveArc ** pData);
typedef struct NNSSndArcWaveArcInfo {
    u32 fileId :24;
    u32 flags  :8;
} NNSSndArcWaveArcInfo;
const NNSSndArcWaveArcInfo * native_fn_02038eb4(int waveArcNo);
void * native_fn_0203917c(u32 fileId);
SNDWaveArc * native_fn_020395d0(u32 fileId, NNSSndHeapHandle heap, BOOL bSetAddr);
SNDWaveArc * native_fn_0203963c(u32 fileId, NNSSndHeapHandle heap, BOOL bSetAddr);
SNDWaveArc * native_fn_020395d0 (u32 fileId, NNSSndHeapHandle heap, BOOL bSetAddr);
SNDWaveArc * native_fn_0203963c (u32 fileId, NNSSndHeapHandle heap, BOOL bSetAddr);
