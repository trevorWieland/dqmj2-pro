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
extern u32 native_fn_01ffa824();
extern u32 native_fn_020649ac();
extern u32 native_fn_020649c0();
extern u32 native_fn_020649d4();
extern u32 native_fn_020649e8();
u32 native_main_020895e8(s32 arg0, s32 arg1) {
    if (arg0 == (u8) native_fn_01ffa824()) {
        if (arg1 < 3) {
            return native_fn_020649ac(arg1);
        }
        return native_fn_020649d4(arg1 - 3);
    }
    if (arg1 < 3) {
        return native_fn_020649c0(arg1);
    }
    return native_fn_020649e8(arg1 - 3);
}
