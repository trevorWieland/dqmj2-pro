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
extern u32 native_fn_0202ac08();
extern u32 native_fn_0202ac4c();
extern u32 native_fn_0205d6f4();
extern u32 native_fn_0205d718();
extern u32 native_fn_0205d790();
extern u32 native_fn_ov001_021d7e80();
extern u32 native_fn_ov001_021db788();
extern u32 native_fn_ov001_021dbb9c();
extern u32 native_fn_ov001_021dc230();
extern u32 native_fn_ov001_021eea10();
extern u32 native_fn_ov001_021eeb70();
extern u32 native_fn_ov001_021eec7c();
typedef struct {
    u8 unknown_0[0x8];
    s8 field_8;
    u8 unknown_9[0x21];
    u8 field_2a;
    s8 field_2b;
    s8 field_2c;
    u8 unknown_2d[0x53];
    s32 field_80;
} Record_native_data_ov001_022388ec;
extern Record_native_data_ov001_022388ec native_data_ov001_022388ec;
extern u8 native_data_ov001_0223896c[];
extern u8 native_data_ov001_02238988[];
