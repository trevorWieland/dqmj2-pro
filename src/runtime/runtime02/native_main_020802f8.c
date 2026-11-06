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
extern u32 native_fn_02008d78();
extern u32 native_fn_02044ff4();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_0207f860();
extern u8 native_data_021c6de8[];
u32 native_main_020802f8(void *arg0) {
    native_fn_02008d78(native_data_021c6de8, 0, 0x14);
    native_fn_02044ff4(native_data_021c6de8, M2C_FIELD(arg0, s16 *, 2), M2C_FIELD(arg0, u8 *, 4));
    native_fn_0207f860(native_data_021c6de8, 0);
    return native_fn_0205e7a8(-1, 0x52);
}
