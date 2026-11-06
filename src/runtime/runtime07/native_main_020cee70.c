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
extern u32 native_fn_02046150();
extern u32 native_fn_02048e74();
extern u32 native_fn_02048fcc();
extern u32 native_fn_0207e97c();
extern u32 native_fn_020c40b8();
extern u32 native_fn_020c40e8();
extern u32 native_fn_020cc3fc();
extern u32 native_fn_020cc740();
extern u8 native_data_021d69b0[];
extern u8 native_data_021d69c4[];
u32 native_main_020cee70(void) {
    void *temp_r0;

    native_fn_02048e74(native_data_021d69c4, 3);
    native_fn_020cc740();
    native_fn_02048fcc();
    native_fn_020cc3fc();
    native_fn_020c40e8();
    native_fn_020c40b8();
    native_fn_02046150(2, 2, 2);
    native_fn_0207e97c();
    M2C_FIELD(native_data_021d69b0, s32 *, 0x18) = 0;
    *(s32 *) native_fn_020cc740() = 0;
    temp_r0 = (void *) native_fn_020cc740();
    M2C_FIELD(temp_r0, s8 *, 0x10) = 3;
    return (u32) temp_r0;
}
