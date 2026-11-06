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
extern u32 native_fn_02085270();
extern u32 native_fn_02086948();
extern u32 native_fn_02086b14();
extern u32 native_fn_02086b68();
extern u32 native_fn_02087674();
extern u8 native_data_021c9698[];
u32 native_main_020867b0(void *arg0) {
    native_fn_02086948(arg0, 0);
    native_fn_02085270(arg0 + 0x3C, (s32) ((0x80 - native_fn_02087674(native_data_021c9698, arg0 + 0x3C, 0)) << 0xF) >> 0x10, 0);
    native_fn_02086b68(arg0, M2C_FIELD(arg0, s32 *, 0x64), M2C_FIELD(arg0, u16 *, 0x6C));
    native_fn_02086b14(arg0, 0);
    return 1U;
}
