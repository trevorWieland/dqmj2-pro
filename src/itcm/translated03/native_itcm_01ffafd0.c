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
extern u32 native_fn_01ffafb8();
extern u32 native_fn_01ffb34c();
extern u32 native_fn_01ffb35c();
extern u32 native_fn_020414c8();
extern u32 native_fn_02041538();
extern u32 native_fn_02041908();
extern u32 native_fn_0204b61c();
extern u8 native_data_021cebe0[];
u32 native_itcm_01ffafd0(void) {
    if (!(M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2) & 0xFF7)) {
        return 0U;
    }
    native_fn_01ffafb8();
    native_fn_0204b61c(native_fn_01ffb34c(), 1);
    native_fn_02041538(0, 2, 8);
    native_fn_02041908(8, 0xA);
    native_fn_020414c8(0x3F);
    M2C_FIELD(native_data_021cebe0, s32 *, 0x20) = 0;
    return 1U;
}
