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
extern u32 native_arm7_fn_037fc558(void);
extern u32 native_arm7_fn_037fc96c(u32);
extern u32 native_arm7_fn_037fbd64(u32, u32);
extern u32 native_arm7_fn_037fbe4c(u32);
extern u32 native_arm7_fn_037fc2e4(u32);
extern u32 native_arm7_fn_037fc590(void);
extern u32 native_arm7_fn_037fdd00(void);
extern u32 native_arm7_fn_037fbe90(void);
extern u32 native_arm7_fn_037fdd14(u32);
extern u32 native_arm7_fn_037fde70(void);
extern u32 native_arm7_data_038076f0;
u32 native_arm7_wram_037fc220(void) {
    u32 temp_r0;
    u32 temp_r4;
    u32 temp_r4_2;

    temp_r4 = *M2C_FIELD(&native_arm7_data_038076f0, u32 **, 8);
    native_arm7_fn_037fc558();
    native_arm7_fn_037fc96c(temp_r4);
    temp_r0 = M2C_FIELD(temp_r4, u32 *, 0x5C);
    if (temp_r0 != 0) {
        native_arm7_fn_037fbd64(temp_r0, temp_r4);
    }
    native_arm7_fn_037fbe4c(temp_r4);
    M2C_FIELD(temp_r4, s32 *, 0x48) = 2;
    native_arm7_fn_037fc2e4(temp_r4 + 0x80);
    native_arm7_fn_037fc590();
    temp_r4_2 = native_arm7_fn_037fdd00();
    native_arm7_fn_037fbe90();
    native_arm7_fn_037fdd14(temp_r4_2);
    return native_arm7_fn_037fde70();
}
