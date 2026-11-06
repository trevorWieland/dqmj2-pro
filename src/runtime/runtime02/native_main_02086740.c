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
extern u32 native_fn_02086b14();
extern u32 native_fn_02086b68();
extern u32 native_fn_02087e44();
u32 native_main_02086740(void *arg0) {
    s16 temp_r2;
    s32 temp_r2_2;

    temp_r2 = M2C_FIELD(arg0, s16 *, 0x70);
    M2C_FIELD(arg0, s16 *, 0x70) = (s16) (temp_r2 + (s16) (((s32) (M2C_FIELD(arg0, s32 *, 0x94) - temp_r2) >> 2) + 1));
    M2C_FIELD(arg0, s16 *, 0x78) = 0;
    native_fn_02087e44(M2C_FIELD(arg0, s32 *, 0x44));
    native_fn_02086b68(arg0, M2C_FIELD(arg0, s32 *, 0x64), M2C_FIELD(arg0, u16 *, 0x6C));
    temp_r2_2 = M2C_FIELD(arg0, s32 *, 0x94);
    if ((s32) M2C_FIELD(arg0, s16 *, 0x70) >= temp_r2_2) {
        M2C_FIELD(arg0, s16 *, 0x70) = (s16) temp_r2_2;
        native_fn_02086b14(arg0, 0);
    }
    return 1U;
}
