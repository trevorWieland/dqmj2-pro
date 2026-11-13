typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct ActorPrefix { u8 unknown0[0x31e]; u8 field31e; } ActorPrefix;
extern void native_fn_ov001_021d7e80(ActorPrefix *);
extern void native_fn_ov001_021f1294(u32, u32);
extern void ov001_begin_state_transition_021f1354(u32, u32, u32, u32);
extern u32 native_fn_ov001_021f1414(s32);
extern u32 ov001_select_mode_id_021f1438(u32);
extern void native_fn_ov001_021f1324(void);
extern void ov001_clear_state_flag4_021f14a4(void);
typedef struct StateView {
 u8 unknown0[0x1b]; u8 field1b; u8 unknown1c; u8 counter1d; u8 state1e;
 u8 unknown1f[0x84-0x1f]; ActorPrefix *actor84;
} StateView;
extern StateView native_data_ov001_0223989c;
u32 native_ov001_021f8c50(u32);
