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
extern u32 native_fn_020414b0();
extern u32 native_fn_020414c8();
extern u32 native_fn_02041510();
extern u32 native_fn_02041538();
extern u32 native_fn_020443c4();
extern u32 native_fn_0205f210();
extern u32 native_fn_020bef48();
extern u32 native_fn_020befb8();
extern u32 native_fn_ov005_021dd788();
extern u32 native_fn_ov005_021e155c();
extern u32 native_fn_ov005_021e6360();
typedef struct {
    u8 unknown_0[0x38];
    s32 field_38;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
u32 native_ov005_021e2f2c(void) {
    u32 temp_r0;
    u32 temp_r0_2;

    temp_r0_2 = native_fn_ov005_021e6360();
    if (temp_r0_2 == 0) {
        return temp_r0_2;
    }
    native_fn_020befb8(0);
    if (native_fn_ov005_021dd788() != 1) {
        temp_r0 = native_fn_ov005_021dd788();
        if (temp_r0 != 0x12) {
            return temp_r0;
        }
    }
    native_data_ov005_021ed438.field_38 = 4;
    native_fn_ov005_021e155c(0x3D);
    native_fn_020443c4(9);
    native_fn_020bef48(1);
    native_fn_020414c8(0x3F);
    native_fn_02041538(1, 2, 0x3C);
    native_fn_020414b0(0x3F);
    native_fn_02041510(1, 2, 0x3C);
    return native_fn_0205f210(0, 0x1E);
}
