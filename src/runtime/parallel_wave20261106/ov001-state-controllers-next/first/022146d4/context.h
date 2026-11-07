typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct ActorPrefix { u8 unknown0[0x31e]; u8 field31e; } ActorPrefix;
extern void native_fn_ov001_021d7e80(ActorPrefix *);
extern void native_fn_ov001_021f1294(u32, u32);
extern void native_fn_ov001_021f1354(u32, u32, u32, u32);
extern u32 native_fn_ov001_021f1414(s32);
extern u32 native_fn_ov001_021f1438(u32);
extern void native_fn_ov001_021f1324(void);
extern void native_fn_ov001_021f14a4(void);
typedef struct StateView {
 u8 unknown0[2]; u8 field2; u8 unknown3[5]; u8 counter8; u8 state9;
 u8 unknownA[6]; ActorPrefix *actor10;
} StateView;
extern StateView native_data_ov001_02242b50;
u32 native_ov001_022146d4(u32);
