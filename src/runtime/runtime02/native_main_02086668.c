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
extern u32 native_fn_0202a634();
extern u32 native_fn_020850a0();
extern u32 native_fn_02086b14();
extern u32 native_fn_02087e44();
u32 native_main_02086668(void *arg0) {
    native_fn_0202a634();
    if ((M2C_FIELD(arg0, s32 *, 0x18) & 4) != 4) {
        native_fn_02087e44(M2C_FIELD(arg0, s32 *, 0x44), 0);
        native_fn_020850a0(arg0);
        M2C_FIELD(arg0, s8 *, 0x36) = (s8) ((s32) (M2C_FIELD(arg0, u8 *, 0x34) + 0x10) >> 4);
        M2C_FIELD(arg0, s8 *, 0x37) = (s8) ((s32) (M2C_FIELD(arg0, u8 *, 0x35) + 0x10) >> 4);
        native_fn_02086b14(arg0, 9);
    }
    return 1U;
}
