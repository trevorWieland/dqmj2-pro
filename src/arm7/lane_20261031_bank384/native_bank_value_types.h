typedef unsigned char u8;
typedef signed short s16;
typedef unsigned short u16;
typedef signed int s32;
typedef unsigned int u32;
typedef int BOOL;
#define FALSE 0
#define TRUE 1
#define SND_INST_MAX_KEYSPLIT 8
#define SND_INST_ILLEGAL 0
#define SND_INST_PCM 1
#define SND_INST_PSG 2
#define SND_INST_NOISE 3
#define SND_INST_DIRECTPCM 4
#define SND_INST_DUMMY 5
#define SND_INST_DRUM_TABLE 16
#define SND_INST_KEY_SPLIT 17
#define SND_INST_OFFSET_TYPE(off) ((u8)(off))
#define SND_INST_OFFSET_NORMAL(bank,off) ((struct SNDInstParam *)((u8 *)(bank)+(u32)(off)))
#define SND_INST_OFFSET_DRUMS(bank,off) ((struct SNDDrumSet *)((u8 *)(bank)+(u32)(off)))
#define SND_INST_OFFSET_KEYSPL(bank,off) ((struct SNDKeySplit *)((u8 *)(bank)+(u32)(off)))
struct SNDInstParam { u16 wave[2]; u8 rootKey,envAttack,envDecay,envSustain,envRelease,pan; };
struct SNDInstData { u8 type,padding; struct SNDInstParam param; };
struct SNDDrumSet { u8 minKey,maxKey; struct SNDInstData instruments[]; };
struct SNDKeySplit { u8 key[8]; struct SNDInstData instruments[]; };
struct SNDBankData { u8 prefix[0x38]; u32 instCount; u32 instOffsets[]; };
struct SNDTrack { u8 prefix[0x28]; const u8 *cur; u8 tail[0x14]; };
struct SNDPlayer { u8 bytes[36]; };
typedef char ParamSize[(sizeof(struct SNDInstParam)==10)?1:-1];
typedef char InstSize[(sizeof(struct SNDInstData)==12)?1:-1];
typedef char TrackSize[(sizeof(struct SNDTrack)==64)?1:-1];
extern void native_host_arm7_arm_037fefe4(void);
extern void native_host_arm7_arm_037fefe8(void);
extern u8 native_host_arm7_arm_03800290(struct SNDTrack *);
extern s16 *native_host_arm7_arm_03801840(const struct SNDPlayer *,int);
extern u16 native_host_arm7_arm_037feec4(void);
#define SNDi_LockMutex native_host_arm7_arm_037fefe4
#define SNDi_UnlockMutex native_host_arm7_arm_037fefe8
#define TrackReadU8 native_host_arm7_arm_03800290
#define PlayerGetVariablePointer native_host_arm7_arm_03801840
#define SND_CalcRandom native_host_arm7_arm_037feec4
enum { SND_SEQ_VAL_U8=0,SND_SEQ_VAL_U16=1,SND_SEQ_VAL_VLV=2,SND_SEQ_VAL_RAN=3,SND_SEQ_VAL_VAR=4 };
