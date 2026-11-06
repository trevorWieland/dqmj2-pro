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
extern u32 native_arm7_fn_037fdd14(u32);
extern u32 native_arm7_fn_037fc2e4(u32);
extern u32 native_arm7_data_03809930;
extern u32 native_arm7_data_03809dc4;
u32 native_arm7_wram_038039e8(u32 arg0) {
    u32 temp_r0;
    u32 var_r0;

    var_r0 = arg0;
    if (M2C_FIELD(&native_arm7_data_03809930, s32 *, 4) != 0) {
        if ((M2C_FIELD(&native_arm7_data_03809930, s32 *, 8) == 4) && (M2C_FIELD(&native_arm7_data_03809930, s32 *, 0x49C) == var_r0)) {
            temp_r0 = native_arm7_fn_037fdd00();
            M2C_FIELD(&native_arm7_data_03809930, s32 *, 8) = 5;
            M2C_FIELD(&native_arm7_data_03809930, s32 *, 4) = 0;
            M2C_FIELD(&native_arm7_data_03809930, s32 *, 0x49C) = 0;
            native_arm7_fn_037fdd14(temp_r0);
            var_r0 = native_arm7_fn_037fc2e4((u32) &native_arm7_data_03809dc4);
            
            return var_r0;
        }
        return var_r0;
    }
    return var_r0;
}
