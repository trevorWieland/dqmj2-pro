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
extern u32 native_fn_0207afec(u32 arg0);
extern u32 native_fn_0207b6e8(u32 arg0);
extern u32 native_fn_0207b748(u32 arg0);
extern u32 ov001_side_slot_record_021db438(u32,u32);
extern u32 ov001_record_is_active_021db8d0(u32);
extern u32 native_fn_ov001_021db918();
extern u32 native_fn_ov001_021f1bf0(u32 arg0);
extern u32 native_fn_ov001_021f1c68(u32 arg0);
extern u32 native_fn_ov001_021f90b4();
extern u32 native_fn_ov001_021f9248(u32 arg0, u32 arg1, u32 arg2, u32 arg3);
extern u32 native_fn_ov001_021f9264(u32 arg0);
extern u32 native_fn_ov001_02216cfc();
extern u32 native_fn_ov001_022170f4();
extern u32 native_fn_ov001_02217910(u32 arg0);
extern u32 native_fn_ov001_02217920();
extern u8 native_data_ov001_022388ec[];
extern u8 native_data_ov001_022389bc[];
