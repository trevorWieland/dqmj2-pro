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
extern u32 native_fn_02061260();
extern u32 native_fn_020620e8();
extern u32 native_fn_0207e720();
extern u32 native_fn_020cba38();
extern u32 native_fn_020cc76c();
extern u32 native_fn_020cf26c();
extern u32 native_fn_020cf27c();
extern u8 native_data_021d69b0[];
extern u8 native_data_021d69b4[];
u32 native_main_020cf094(void) {
    u32 temp_r0;
    u32 temp_r4;

    temp_r0 = native_fn_020cf27c();
    M2C_FIELD(native_data_021d69b0, s8 *, 4) = 4;
    M2C_FIELD(native_data_021d69b0, u32 *, 0xC) = temp_r0;
    M2C_FIELD(native_data_021d69b0, s8 *, 0x10) = 0x14;
    M2C_FIELD(native_data_021d69b0, s8 *, 0x11) = 1;
    native_fn_0207e720(native_data_021d69b4);
    native_fn_02061260(0);
    native_fn_020620e8(0x20, 1);
    temp_r4 = native_fn_020cf26c();
    return native_fn_020cba38(temp_r4, native_fn_020cc76c());
}
