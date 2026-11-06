typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed short int s16;
typedef int BOOL;
BOOL native_fn_02009a0c(u32 tag);
void native_fn_02009108(int playerNo);
void native_fn_02009148(int playerNo, int volume);
u32 native_fn_02009ce8(void);
extern const s16 native_data_main_020d8254[128 ];
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
void * native_fn_0202bb88(NNSFndList * list, void * object);
struct NNSSndHeap;
typedef struct NNSSndHeap * NNSSndHeapHandle;
typedef struct NNSSndFader {
    int origin;
    int target;
    int counter;
    int frame;
} NNSSndFader;
int native_fn_020379ec(const NNSSndFader * fader);
void native_fn_02037a20(NNSSndFader * fader);
BOOL native_fn_02037a38(const NNSSndFader * fader);
struct NNSSndSeqPlayer;
struct NNSSndPlayer;
struct NNSSndPlayerHeap;
enum NNSSndSeqPlayerStatus {
    NNS_SND_SEQ_PLAYER_STATUS_STOP,
    NNS_SND_SEQ_PLAYER_STATUS_PLAY,
    NNS_SND_SEQ_PLAYER_STATUS_FADEOUT
};
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
void native_main_020382fc(void);
typedef struct NNSSndPlayerHeap {
    NNSFndLink link;
    NNSSndHeapHandle handle;
    NNSSndSeqPlayer * player;
    int playerNo;
} NNSSndPlayerHeap;
typedef struct {
NNSFndList field_0000;
NNSFndList field_000c;
NNSSndSeqPlayer field_0018[ 16 ];
NNSSndPlayer field_0458[ 32 ];
} NativeStorage_020f4360;
extern NativeStorage_020f4360 native_data_main_020f4360;
void native_fn_020387a8(NNSSndSeqPlayer * seqPlayer);
void native_fn_02038708(NNSSndSeqPlayer * seqPlayer);
void native_fn_02038708 (NNSSndSeqPlayer * seqPlayer);
void native_fn_020387a8 (NNSSndSeqPlayer * seqPlayer);
static inline
s16 SND_CalcDecibel (int scale)
{
	((void) 0) ;
	return native_data_main_020d8254[scale];
}
