typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed short int s16;
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
struct SNDBankData;
typedef struct {
    void * prevObject;
    void * nextObject;
} NNSFndLink;
typedef struct {
    void * headObject;
    void * tailObject;
    u16 numObjects;
    u16 offset;
} NNSFndList;
struct NNSSndHeap;
typedef struct NNSSndHeap * NNSSndHeapHandle;
struct NNSSndHandle;
typedef struct NNSSndSeqParam {
    u16 bankNo;
    u8 volume;
    u8 channelPrio;
    u8 playerPrio;
    u8 playerNo;
    u16 reserved;
} NNSSndSeqParam;
typedef struct NNSSndSeqData {
    struct SNDBinaryFileHeader fileHeader;
    struct SNDBinaryBlockHeader blockHeader;
    u32 baseOffset;
    u32 data[0];
} NNSSndSeqData;
typedef struct NNSSndArcSeqInfo {
    u32 fileId;
    struct NNSSndSeqParam param;
} NNSSndArcSeqInfo;
typedef struct NNSSndFader {
    int origin;
    int target;
    int counter;
    int frame;
} NNSSndFader;
struct SNDBankData;
struct NNSSndSeqPlayer;
struct NNSSndPlayer;
struct NNSSndPlayerHeap;
typedef struct NNSSndHandle {
    struct NNSSndSeqPlayer * player;
} NNSSndHandle;
typedef struct NNSSndSeqPlayer {
    struct NNSSndHandle * handle;
    struct NNSSndPlayer * player;
    struct NNSSndPlayerHeap * heap;
    NNSFndLink playerLink;
    NNSFndLink prioLink;
    NNSSndFader fader;
    u8 status;
    u8 startFlag;
    u8 pauseFlag;
    u8 prepareFlag;
    u32 commandTag;
    u16 seqType;
    u16 pad2;
    u16 seqNo;
    u16 seqArcIndex;
    u8 playerNo;
    u8 prio;
    s16 volume;
    u8 initVolume;
    u8 extVolume;
    u16 pad3_;
} NNSSndSeqPlayer;
typedef struct NNSSndPlayer {
    NNSFndList playerList;
    NNSFndList heapList;
    u32 playableSeqCount;
    u32 allocChBitFlag;
    u8 volume;
    u8 pad_;
    u16 pad2_;
} NNSSndPlayer;
void native_fn_02038134(NNSSndHandle * handle, int volume);
void native_fn_02038174(NNSSndHandle * handle, int priority);
void native_fn_020381d4(NNSSndHandle * handle, int seqNo);
void native_fn_02038504(NNSSndSeqPlayer * seqPlayer, const void * seqDataBase, u32 seqDataOffset, const struct SNDBankData * bank);
NNSSndSeqPlayer * native_fn_02038460(NNSSndHandle * handle, int playerNo, int prio);
void native_fn_020384f8(NNSSndSeqPlayer * seqPlayer);
NNSSndHeapHandle native_fn_020385c8(int playerNo, NNSSndSeqPlayer * seqPlayer);
struct NNSSndSeqData;
struct SNDBankData;
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
NNSSndArcLoadResult native_fn_02039208(int seqNo, u32 loadFlag, NNSSndHeapHandle heap, BOOL bSetAddr, struct NNSSndSeqData ** pData);
NNSSndArcLoadResult native_fn_0203928c(int bankNo, u32 loadFlag, NNSSndHeapHandle heap, BOOL bSetAddr, struct SNDBankData ** pData);
BOOL native_main_02039ba0(NNSSndHandle * handle, int playerNo, int bankNo, int playerPrio, const NNSSndArcSeqInfo * info, int seqNo);
