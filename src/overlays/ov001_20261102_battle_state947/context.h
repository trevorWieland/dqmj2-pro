typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
#define NULL ((void *)0)
extern u32 native_fn_0202ac08();
extern u32 native_fn_0202ac4c();
extern u32 native_fn_0205d6f4(u32 arg0);
extern u32 native_fn_0205d718(u32 arg0);
extern u32 native_fn_0205d790(u32);
extern u32 native_fn_ov001_021d7e80(u32 arg0);
extern u32 native_fn_ov001_021db788();
extern u32 ov001_record_is_active_021db8d0(u32);
extern u32 native_fn_ov001_021dbb9c(u32 arg0, u32 arg1);
extern u32 native_fn_ov001_021dc230();
extern u32 native_fn_ov001_021dda80();
extern u32 native_fn_ov001_021eea10();
extern u32 native_fn_ov001_021eeb70(u32);
extern u32 ov001_effect_resource_create_021eec7c(u32 arg0, u32 arg1, u32 arg2);
extern u32 native_fn_ov001_021f1294();
extern u32 native_fn_ov001_021f1324();
extern u32 ov001_begin_state_transition_021f1354();
extern u32 native_fn_ov001_021f1414(u32 arg0);
extern u32 ov001_select_mode_id_021f1438(u32 arg0);
extern u32 ov001_clear_state_flag4_021f14a4();
extern u32 native_fn_ov001_021ff238();
extern u8 native_data_ov001_022388ec[];
extern u32 native_data_ov001_02238950[];
extern u8 native_data_ov001_02238988[];
