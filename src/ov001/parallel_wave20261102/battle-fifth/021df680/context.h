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
extern u32 native_fn_ov001_021d7e80();
extern u32 native_fn_ov001_021dcfa0();
extern u32 native_fn_ov001_021f1294();
extern u32 native_fn_ov001_021f1324();
extern u32 ov001_begin_state_transition_021f1354();
extern u32 ov001_select_mode_id_021f1438();
extern u32 ov001_clear_state_flag4_021f14a4();
extern u32 native_fn_ov001_021f14e4();
extern u8 native_data_ov001_022388ec[];
