#define NULL ((void *)0)
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
extern u32 native_fn_020975b8();
extern u32 native_fn_02097618();
extern u32 native_fn_0209aa64();
extern u8 native_data_021d1b68[];
u32 native_main_0209c640(void) {
    if (M2C_FIELD(M2C_FIELD(native_data_021d1b68, void **, 4), s32 *, 0x24) != 0) {
        native_fn_020975b8();
        native_fn_02097618();
        native_fn_0209aa64(0, M2C_FIELD(M2C_FIELD(native_data_021d1b68, void **, 4), s32 *, 0x24), 0);
        M2C_FIELD(M2C_FIELD(native_data_021d1b68, void **, 4), s32 *, 0x24) = 0;
    }
    M2C_FIELD(native_data_021d1b68, void **, 4) = NULL;
    return (u32) native_data_021d1b68;
}
