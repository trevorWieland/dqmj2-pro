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
    u8 unknown_0[0x40];
    s32 field_40;
    u8 unknown_44[0x4];
    s32 field_48;
} Record_native_data_ov000_02245e54;
extern Record_native_data_ov000_02245e54 native_data_ov000_02245e54;
u32 native_ov000_02219c88(void) {
    s32 temp_r1;

    temp_r1 = (0x1FF & (s16) (((s32) native_data_ov000_02245e54.field_40 >> 0xC) - 0x80)) | (0x01FF0000 & ((s16) (((s32) native_data_ov000_02245e54.field_48 >> 0xC) - 0x60) << 0x10));
    M2C_FIELD((void *)0x04001014, s32 *, 0) = temp_r1;
    M2C_FIELD((void *)0x04001014, s32 *, 4) = temp_r1;
    M2C_FIELD((void *)0x04001014, s32 *, 8) = temp_r1;
    return 0x04001014U;
}
