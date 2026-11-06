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
extern u32 native_fn_020363d0();
u32 native_main_020852d0(void *arg0, u8 arg1) {
    M2C_FIELD(arg0, u8 *, 0x84) = arg1;
    return native_fn_020363d0(M2C_FIELD(arg0, s32 *, 0x54), M2C_FIELD(arg0, u8 *, 0x5E), M2C_FIELD(arg0, u8 *, 0x5F), M2C_FIELD(arg0, u8 *, 0x5C), (s32) M2C_FIELD(arg0, u8 *, 0x5D), 0x20, M2C_FIELD(arg0, s32 *, 0x58), (s32) M2C_FIELD(arg0, u8 *, 0x84));
}
