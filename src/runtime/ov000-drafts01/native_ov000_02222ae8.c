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
extern u32 native_fn_0201d444();
extern u32 native_fn_020414b0();
extern u32 native_fn_02041510();
extern u32 native_fn_02041560();
extern u32 native_fn_020642dc();
extern u32 native_fn_ov000_02223328();
extern u32 native_fn_ov000_02223390();
extern u8 native_data_ov000_0222fca4[];
extern u8 native_data_ov000_02246574[];
u32 native_ov000_02222ae8(void) {
    u8 sp0[32];
    s32 temp_r0;

    native_fn_0201d444(&sp0, native_data_ov000_0222fca4);
    native_fn_ov000_02223390(&sp0);
    temp_r0 = (s32) native_fn_020642dc();
    if (temp_r0 <= 1) {
        if (temp_r0 != 1) {
            goto block_10;
        }
        goto block_9;
    }
    if ((temp_r0 <= 0x1B) && (temp_r0 >= 0x19)) {
        if ((temp_r0 != 0x19) && (temp_r0 != 0x1A) && (temp_r0 != 0x1B)) {
            goto block_10;
        }
block_9:
        native_fn_ov000_02223328();
    } else {
block_10:
        native_fn_02041560(0xA);
        native_fn_02041510(0, 2, 0xA);
    }
    native_fn_020414b0(0x28);
    *native_data_ov000_02246574 = 2;
    return 0U;
}
