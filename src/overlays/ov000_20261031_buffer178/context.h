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
extern void native_fn_02008be0(u32, void *, u32);
extern u32 native_fn_02046af4();
extern u32 native_fn_020470fc(const u16 *);
extern u32 native_fn_020852b0(void *, s32);
extern u32 native_fn_02087674();
extern u32 native_fn_02087a48();
extern u8 native_data_021c9698[];
extern u8 native_data_ov000_02238514[];
typedef struct {
    s16 field_0;
    s16 field_2;
    u8 unknown_4[0x4];
    s8 field_8;
    u8 field_9;
    u8 field_a;
} Record_native_data_ov000_02238520;
extern Record_native_data_ov000_02238520 native_data_ov000_02238520;
extern u8 native_data_ov000_0223852b[];
