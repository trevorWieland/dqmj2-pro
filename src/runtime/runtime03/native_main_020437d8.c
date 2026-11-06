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
extern u32 native_fn_02041d20();
extern u32 native_fn_02043678();
extern u32 native_fn_02065364();
extern u32 native_fn_ov001_021d8ab0();
extern u32 native_fn_ov001_021d8b88();
extern u32 native_fn_ov001_021d90f8();
extern u32 native_fn_ov001_021d939c();
extern u32 native_fn_ov001_021e3270();
extern u32 native_fn_ov001_021e32a0();
extern u32 native_fn_ov001_021f1088();
extern u32 native_fn_ov001_021f92d8();
extern u32 native_fn_ov001_021fc110();
extern u32 native_fn_ov001_02217e54();
extern u8 native_data_020f69c4[];
u32 native_main_020437d8(void) {
    native_fn_ov001_021d939c();
    native_fn_ov001_021d90f8();
    native_fn_ov001_021f92d8();
    native_fn_02043678();
    native_fn_ov001_021d8ab0(-1);
    native_fn_ov001_021d8b88(0);
    native_fn_02041d20();
    native_fn_ov001_021e3270();
    native_fn_ov001_021e32a0();
    if (native_fn_02065364() != -1U) {
        native_fn_ov001_02217e54();
    }
    native_fn_ov001_021f1088();
    native_fn_ov001_021fc110();
    M2C_FIELD(native_data_020f69c4, u8 *, 0) = 0;
    M2C_FIELD(native_data_020f69c4, s8 *, 3) = 3;
    return 1U;
}
