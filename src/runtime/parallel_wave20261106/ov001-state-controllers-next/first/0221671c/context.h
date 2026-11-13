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
extern u32 ov001_begin_state_transition_021f1354(u32,u32,u32,u32);
extern u32 native_fn_ov001_021f1414(s32);
extern u32 ov001_select_mode_id_021f1438(u32);
extern u32 ov001_clear_state_flag4_021f14a4(void);
extern u32 native_fn_ov001_021f14e4(void);
extern u32 native_fn_ov001_021f1324(void);
extern u32 native_fn_ov001_021d7e80(ActorView *);
typedef struct StateView {
 u8 unknown0; u8 field1; u8 state2; u8 counter3; u16 field4; u8 unknown6[2]; ActorView *actor8;
} StateView;
extern StateView native_data_ov001_02242be8;
extern u32 native_fn_ov001_022025a4(u32,u32);
u32 native_ov001_0221671c(void);
