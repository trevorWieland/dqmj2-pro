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
extern u32 native_arm7_fn_038073f0(void);
extern u32 native_arm7_fn_037fe12c(u32, u32, u32);
extern u32 native_arm7_fn_038073a4(u32);
extern u32 native_arm7_data_027f8884;
u32 native_arm7_main_027e4a94(s32 arg0, s16 arg1, u32 arg2) {
    void *temp_r0;
    void *temp_r5;

    temp_r5 = M2C_FIELD(&native_arm7_data_027f8884, void **, 0x550);
    temp_r0 = (void *) native_arm7_fn_038073f0();
    M2C_FIELD(temp_r0, s16 *, 2) = 0;
    if (arg0 != 0) {
        M2C_FIELD(temp_r0, s16 *, 0) = 8;
        M2C_FIELD(temp_r0, s16 *, 8) = 0x1A;
        M2C_FIELD(temp_r0, u16 *, 0x12) = 0xF001;
        M2C_FIELD(temp_r0, s16 *, 0x10) = arg1;
        native_arm7_fn_037fe12c(arg2, (u32) (temp_r0 + 0xA), 6U);
        M2C_FIELD(temp_r0, u16 *, 0x2C) = (u16) M2C_FIELD(temp_r5, u16 *, 0x30);
        M2C_FIELD(temp_r0, u16 *, 0x2E) = (u16) M2C_FIELD(temp_r5, u16 *, 0x32);
    } else {
        M2C_FIELD(temp_r0, s16 *, 0) = 0xC;
        M2C_FIELD(temp_r0, s16 *, 8) = 0x1A;
        M2C_FIELD(temp_r0, u16 *, 0xC) = 0xF001;
        M2C_FIELD(temp_r0, u16 *, 0xA) = (u16) M2C_FIELD(temp_r5, u16 *, 0x188);
        native_arm7_fn_037fe12c(arg2, (u32) (temp_r0 + 0x10), 6U);
        M2C_FIELD(temp_r0, u16 *, 0x16) = (u16) M2C_FIELD(temp_r5, u16 *, 0x30);
        M2C_FIELD(temp_r0, u16 *, 0x18) = (u16) M2C_FIELD(temp_r5, u16 *, 0x32);
    }
    return native_arm7_fn_038073a4((u32) temp_r0);
}
