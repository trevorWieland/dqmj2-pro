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
typedef struct {
    u8 unknown_0[0x10];
    s32 field_10;
    u8 unknown_14[0x10];
    s32 field_24;
    u8 unknown_28[0xc];
    s32 field_34;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
void native_ov005_021e54e8(u32 arg0, void *arg1) {
    if ((s32) native_data_ov005_021ed438.field_24 > 0) {
        goto block_2;
    }
    return;
block_2:
    if (native_data_ov005_021ed438.field_34 != 1) {
        goto block_4;
    }
    return;
block_4:
    native_data_ov005_021ed438.field_10 = (s32) M2C_FIELD(arg1, s32 *, 0);
    if (M2C_FIELD(arg1, s32 *, 4) == 0) {
        goto block_6;
    }
    native_data_ov005_021ed438.field_34 = 1;
block_6:
    return;
}
