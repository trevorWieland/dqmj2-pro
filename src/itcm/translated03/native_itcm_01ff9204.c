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
extern u32 native_fn_01ffa5ac();
extern u32 native_fn_01ffae9c();
extern u32 native_fn_01ffafb8();
extern u32 native_fn_01ffb35c();
extern u32 native_fn_01ffb378();
extern u32 native_fn_020894e0();
extern u8 native_data_021ceb54[];
extern u8 native_data_021ceb94[];
u32 native_itcm_01ff9204(void) {
    u16 temp_r0;

    if (!(M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2) & 1)) {
        temp_r0 = M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2);
        if (!(temp_r0 & 2)) {
            return (u32) temp_r0;
        }
    }
    native_fn_01ffafb8();
    native_fn_020894e0();
    if ((native_fn_01ffb378() == 1) || (M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2) & 2)) {
        M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 0x15;
        if (M2C_FIELD(native_data_021ceb54, s32 *, 8) == 1) {
            native_fn_01ffae9c(0x10, 6, 0xD, -1);
        } else {
            native_fn_01ffae9c(0x10, 9, 3, -1);
        }
        M2C_FIELD(native_data_021ceb54, s32 *, 0x54) = 2;
    } else {
        M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 0x14;
        M2C_FIELD(native_data_021ceb54, s32 *, 0x54) = 1;
    }
    return native_fn_01ffa5ac(native_data_021ceb94, 0x34, 2);
}
