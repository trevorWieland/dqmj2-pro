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
#define NULL ((void *)0)
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_arm7_fn_037fdd00(void);
extern u32 native_arm7_fn_037fdd14(u32);
extern u32 native_arm7_fn_037fd2c0(u32);
extern u8 native_arm7_data_038078a8;
u32 native_arm7_wram_037fd5c0(void *arg0) {
    u32 temp_r0;
    void *temp_r0_2;
    void *temp_r1;

    temp_r0 = native_arm7_fn_037fdd00();
    if (M2C_FIELD(arg0, s32 *, 0) == 0) {
        return native_arm7_fn_037fdd14(temp_r0);
    }
    temp_r0_2 = M2C_FIELD(arg0, void **, 0x18);
    if (temp_r0_2 == NULL) {
        M2C_FIELD((u32) &native_arm7_data_038078a8, void **, 8) = (void *) M2C_FIELD(arg0, void **, 0x14);
    } else {
        M2C_FIELD(temp_r0_2, void **, 0x14) = (void *) M2C_FIELD(arg0, void **, 0x14);
    }
    temp_r1 = M2C_FIELD(arg0, void **, 0x14);
    if (temp_r1 != NULL) {
        M2C_FIELD(temp_r1, void **, 0x18) = temp_r0_2;
    } else {
        M2C_FIELD((u32) &native_arm7_data_038078a8, void **, 4) = temp_r0_2;
        if (temp_r0_2 != NULL) {
            native_arm7_fn_037fd2c0((u32) temp_r0_2);
        }
    }
    M2C_FIELD(arg0, s32 *, 0) = 0;
    M2C_FIELD(arg0, s32 *, 0x1C) = 0;
    M2C_FIELD(arg0, s32 *, 0x20) = 0;
    return native_arm7_fn_037fdd14(temp_r0);
}
