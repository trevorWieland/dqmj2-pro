typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct ActorView {
 u8 unknown0[0x1e8]; u8 *child1e8; u8 unknown1ec[0x31e - 0x1ec];
 u8 field31e; u8 field31f; u8 unknown320[5]; u8 field325;
} ActorView;
extern u32 native_fn_ov001_021f1294(u32,u32);
extern u32 native_fn_ov001_021f1354(u32,u32,u32,u32);
extern u32 native_fn_ov001_021f1414(s32);
extern u32 native_fn_ov001_021f1438(u32);
extern u32 native_fn_ov001_021f14a4(void);
extern u32 native_fn_ov001_021f14e4(void);
extern u32 native_fn_ov001_021f1324(void);
extern u32 native_fn_ov001_021d7e80(ActorView *);
typedef struct StateView {
 u8 unknown0[0x11]; u8 counter11; u8 unknown12; u8 field13;
 u8 unknown14[0x23 - 0x14]; u8 state23; u8 unknown24[0x36 - 0x24];
 u16 field36; u8 unknown38[0x60 - 0x38]; ActorView *actor60;
} StateView;
extern StateView native_data_ov001_02238d7c;
extern u32 native_fn_ov001_021eaa3c(u32);
extern u32 native_fn_ov001_021eaa88(u32);
u32 native_ov001_021edd10(u32);
