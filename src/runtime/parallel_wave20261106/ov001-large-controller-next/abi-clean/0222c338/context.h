typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;
typedef struct Object440 {
    u8 unknown0[0x234];
    s8 field234;
    u8 unknown235[0x440 - 0x235];
} Object440;
typedef struct ControllerView {
    u8 selector0;
    u8 field1;
    u8 unknown2[5];
    u8 counter7;
    u8 state8;
} ControllerView;
extern ControllerView native_data_022497e8;
extern void *native_fn_0207afec(s32);
extern void native_fn_ov001_021d7f54(u32);
extern void ov001_begin_state_transition_021f1354(u32, u32, u32, u32);
extern u32 native_fn_ov001_021f1414(s32);
extern u32 ov001_select_mode_id_021f1438(u32);
extern void ov001_clear_state_flag4_021f14a4(void);
extern Object440 *ov001_side_slot_record_021db438(s32, u32);
extern u32 ov001_record_is_active_021db8d0(Object440 *);
extern void native_fn_ov001_021dbf98(Object440 *, s32, s32, s32, s32);
extern void native_fn_ov001_021ee91c(Object440 *, s32);
u32 native_ov001_0222c338(void);
