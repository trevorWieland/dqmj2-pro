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
extern u32 native_arm7_fn_037fdd00(void);
extern u32 native_arm7_fn_037fbcec(u32, u32);
extern u32 native_arm7_fn_037fbe90(void);
extern u32 native_arm7_fn_037fdd14(u32);
extern u32 native_arm7_data_038076f0;
u32 native_arm7_wram_037fc290(u32 arg0) {
    u32 temp_r4;
    void *temp_r5;

    temp_r4 = native_arm7_fn_037fdd00();
    temp_r5 = *M2C_FIELD(&native_arm7_data_038076f0, void ***, 8);
    if (arg0 != 0) {
        M2C_FIELD(temp_r5, u32 *, 0x5C) = arg0;
        native_arm7_fn_037fbcec(arg0, (u32) temp_r5);
    }
    M2C_FIELD(temp_r5, s32 *, 0x48) = 0;
    native_arm7_fn_037fbe90();
    return native_arm7_fn_037fdd14(temp_r4);
}
