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
extern void native_fn_0202a498(s32, void *);
extern u8 native_data_021c672c[];

u32 native_main_0207aad0(s32 arg0) {
    if (M2C_FIELD(native_data_021c672c, void **, 0x10) != NULL) {
        native_fn_0202a498(arg0, M2C_FIELD(native_data_021c672c, void **, 0x10));
        M2C_FIELD(native_data_021c672c, void **, 0x10) = NULL;
    }
    M2C_FIELD(native_data_021c672c, s32 *, 0x14) = 0;
    return (u32) native_data_021c672c;
}
