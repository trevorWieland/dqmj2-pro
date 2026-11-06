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
extern u32 native_fn_020065f0();
extern u32 native_fn_0200698c();
extern u32 native_fn_02007074();
extern u32 native_fn_0202b9dc();
extern u32 native_fn_0203b510();
u32 native_main_0203a6ac(void *arg0, s32 arg1) {
    native_fn_020065f0(arg0, native_fn_0203b510, arg0, arg0 + 0x4C0, 0x400, arg1);
    native_fn_0202b9dc(arg0 + 0x4E0, 0);
    native_fn_02007074(arg0 + 0x4C8);
    M2C_FIELD(arg0, s32 *, 0x4C4) = 0;
    M2C_FIELD(arg0, s32 *, 0x4C0) = 0;
    return native_fn_0200698c(arg0);
}
