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
extern u32 native_fn_020491f8();
extern u32 native_fn_0205e7a8();
extern u8 native_data_ov000_02236d98[];
u32 native_ov000_021f1080(u32 *arg0) {
    s32 temp_r5;
    u32 temp_r0;
    u32 temp_r0_2;

    temp_r5 = M2C_FIELD(M2C_FIELD(native_data_ov000_02236d98, void **, 8), s32 *, 0x14);
    temp_r0_2 = native_fn_020491f8(M2C_FIELD(native_data_ov000_02236d98, void **, 8) + 0x10);
    if (temp_r0_2 == 0) {
        return temp_r0_2;
    }
    if (temp_r5 != M2C_FIELD(M2C_FIELD(native_data_ov000_02236d98, void **, 8), s32 *, 0x14)) {
        native_fn_0205e7a8(-1, 0x56);
    } else {
        native_fn_0205e7a8(-1, 0x55);
    }
    temp_r0 = *arg0 | 1;
    *arg0 = temp_r0;
    return temp_r0;
}
