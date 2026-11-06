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
extern u32 native_fn_020620e8();
extern u32 native_fn_020642dc();
extern u8 native_data_021ceb54[];
u32 native_main_02088588(void) {
    u32 temp_r0;

    M2C_FIELD(native_data_021ceb54, s32 *, 4) = 1;
    if (native_fn_020642dc() == 5) {
        native_fn_020620e8(0, 1);
    }
    temp_r0 = native_fn_020642dc();
    if (temp_r0 != 0x29) {
        return temp_r0;
    }
    return native_fn_020620e8(0, 1);
}
