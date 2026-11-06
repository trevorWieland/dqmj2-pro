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
extern u32 native_arm7_fn_027e7e54(u32);
extern u32 native_arm7_fn_038073f0(void);
extern u32 native_arm7_fn_038073a4(u32);
extern u32 native_arm7_data_027f8884;
u32 native_arm7_main_027e7e04(void *arg0) {
    s32 temp_r2;
    void *temp_r0;
    void *temp_r3;

    temp_r3 = M2C_FIELD(arg0, void **, 4);
    M2C_FIELD(&native_arm7_data_027f8884, void **, 0x54C) = temp_r3;
    temp_r2 = M2C_FIELD(arg0, s32 *, 8);
    M2C_FIELD(&native_arm7_data_027f8884, s32 *, 0x550) = temp_r2;
    M2C_FIELD(temp_r3, s32 *, 0) = temp_r2;
    M2C_FIELD(temp_r3, s32 *, 8) = (s32) M2C_FIELD(arg0, s32 *, 0xC);
    native_arm7_fn_027e7e54(M2C_FIELD(arg0, u32 *, 0x10));
    temp_r0 = (void *) native_arm7_fn_038073f0();
    M2C_FIELD(temp_r0, s16 *, 0) = 3;
    M2C_FIELD(temp_r0, s16 *, 2) = 0;
    return native_arm7_fn_038073a4((u32) temp_r0);
}
