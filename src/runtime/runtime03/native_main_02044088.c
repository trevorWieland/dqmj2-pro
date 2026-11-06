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
extern u32 native_fn_ov001_021e65a8();
extern u8 native_data_020f69c4[];
u32 native_main_02044088(void) {
    u32 temp_r0;

    temp_r0 = native_fn_ov001_021e65a8();
    switch (temp_r0) {
    case 0:
        break;
    case 2:
        M2C_FIELD(native_data_020f69c4, s8 *, 3) = 0xA;
        break;
    case 1:
        M2C_FIELD(native_data_020f69c4, s8 *, 3) = 0xD;
        break;
    }
    return 0U;
}
