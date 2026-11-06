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
extern u32 native_fn_02008d78();
extern u32 native_fn_0202ac08();
extern u32 native_fn_02044424(s32);
extern u32 native_fn_02063c00();
extern void * native_fn_ov001_021db438(s32, u32);
extern u32 native_fn_ov001_021f1294();
typedef struct {
    u8 unknown_0[0x1];
    s8 field_1;
} Record_native_data_ov001_0222ed28;
extern Record_native_data_ov001_0222ed28 native_data_ov001_0222ed28;
extern u8 native_data_ov001_02239a14[];
extern u8 native_data_ov001_02239a8c[];
extern u8 native_data_ov001_02239abc[];
