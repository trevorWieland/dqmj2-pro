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
extern u32 native_fn_020404f0();
extern u32 native_fn_020414b0();
extern u32 native_fn_02041510();
extern u32 native_fn_020418e8();
extern u32 native_fn_0206157c();
u32 native_main_0203f9a4(void) {
    if (native_fn_0206157c() != 0) {
        native_fn_020404f0(4);
        native_fn_02041510(0, 2, 4);
        native_fn_020418e8(4, 0xA);
        native_fn_020414b0(0x3F);
    }
    return 0U;
}
