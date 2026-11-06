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
extern u32 native_fn_02041d78();
extern u32 native_fn_ov001_021d8b00();
extern u32 native_fn_ov001_021d8c9c();
extern u32 native_fn_ov001_021d93b0();
extern u32 native_fn_ov001_021e332c();
extern u32 native_fn_ov001_02218028();
extern u32 native_fn_ov001_0221806c();
extern u8 native_data_020f69c4[];
u32 native_main_0204411c(void) {
    native_fn_ov001_021e332c();
    if (native_fn_ov001_0221806c() != 0) {
        native_fn_ov001_02218028();
    }
    native_fn_ov001_021d8b00();
    native_fn_ov001_021d8c9c();
    native_fn_02041d78();
    native_fn_ov001_021d93b0();
    M2C_FIELD(native_data_020f69c4, s8 *, 3) = 0x11;
    return 1U;
}
