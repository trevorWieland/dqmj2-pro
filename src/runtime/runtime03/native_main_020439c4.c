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
extern u32 native_fn_020438f4();
extern u32 native_fn_020444a8();
extern u32 native_fn_ov000_021e3370();
extern u32 native_fn_ov001_021d8c5c();
extern u32 native_fn_ov001_021da544();
extern u32 native_fn_ov001_021e048c();
extern u32 native_fn_ov001_02217f04();
extern u32 native_fn_ov001_0221806c();
extern u8 native_data_020f69c4[];
u32 native_main_020439c4(void) {
    native_fn_ov000_021e3370();
    if (native_fn_ov001_0221806c() != 0) {
        native_fn_ov001_02217f04();
    }
    native_fn_ov001_021da544();
    if (native_fn_020444a8() != 0) {
        M2C_FIELD(native_data_020f69c4, s8 *, 0x27) = 0;
    } else {
        M2C_FIELD(native_data_020f69c4, s8 *, 0x27) = (s8) native_fn_020438f4();
    }
    native_fn_ov001_021d8c5c();
    native_fn_ov001_021e048c();
    M2C_FIELD(native_data_020f69c4, s8 *, 3) = 5;
    return 1U;
}
