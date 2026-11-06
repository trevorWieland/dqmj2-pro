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
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
extern u32 native_fn_02008be0();
extern u32 native_fn_02049aa8();
extern u32 native_fn_0204a104();
extern u32 native_fn_020877bc();
extern u32 native_fn_02087e44();
u32 native_main_0204a154(u32 arg0, u32 arg1, u32 arg2, u32 arg3, s32 arg4, s32 arg5) {
    u8 sp0[64];
    void *temp_r1;

    temp_r1 = M2C_FIELD(*(void **) native_fn_02049aa8(), void **, 4);
    if (arg5 != 0) {
        native_fn_02087e44(M2C_FIELD(temp_r1, s32 *, 0x44), 0);
    }
    native_fn_02008be0(0, &sp0, 0x40);
    native_fn_020877bc(arg3, &sp0, 0x40, arg4);
    return native_fn_0204a104(arg0, arg1, arg2, &sp0);
}
