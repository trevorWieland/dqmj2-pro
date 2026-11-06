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
extern u32 native_fn_0205fd0c();
extern u32 native_fn_0205fd28();
extern u32 native_fn_0205fd34();
extern u8 native_data_021d6630[];
u32 native_main_020cbb64(void) {
    u32 temp_r0;
    u32 temp_r0_2;

    M2C_FIELD(native_data_021d6630, s8 *, 0xD1) = (s8) (M2C_FIELD(native_data_021d6630, s8 *, 0xD1) & ~0xF0);
    M2C_FIELD(native_data_021d6630, s8 *, 0xD1) = (s8) (M2C_FIELD(native_data_021d6630, s8 *, 0xD1) & ~8);
    native_fn_0205fd34(native_data_021d6630, 0x10);
    temp_r0_2 = native_fn_0205fd28(native_data_021d6630);
    if (temp_r0_2 != 0) {
        return temp_r0_2;
    }
    do {
        M2C_FIELD(native_data_021d6630, s8 *, 0xD1) = (s8) (M2C_FIELD(native_data_021d6630, s8 *, 0xD1) & ~0xF0);
        M2C_FIELD(native_data_021d6630, s8 *, 0xD1) = (s8) (M2C_FIELD(native_data_021d6630, s8 *, 0xD1) & ~8);
        native_fn_0205fd0c(native_data_021d6630);
        temp_r0 = native_fn_0205fd28(native_data_021d6630);
    } while (temp_r0 == 0);
    return temp_r0;
}
