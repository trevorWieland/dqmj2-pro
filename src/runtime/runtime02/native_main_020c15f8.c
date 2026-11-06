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
extern u32 native_fn_02069000();
extern u32 native_fn_0206c1d4();
extern u32 native_fn_020bf6c4();
extern u32 native_fn_020c1a04();
extern u8 native_data_021d4bec[];
u32 native_main_020c15f8(void) {
    s32 sp4;
    u8 sp1;
    u8 sp0;

    native_fn_0206c1d4(native_fn_02069000(), &sp1, &sp0);
    sp4 = (s32) M2C_FIELD(native_data_021d4bec, u8 *, 4);
    return native_fn_020c1a04((sp1 + 0xB) * 8, (sp0 + 1) * 8, &sp4, native_fn_020bf6c4());
}
