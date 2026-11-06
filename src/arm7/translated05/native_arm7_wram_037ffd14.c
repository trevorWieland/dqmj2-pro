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
extern u32 native_arm7_fn_037fea20(u32, u32);
extern u32 native_arm7_data_03807ee0;
void native_arm7_wram_037ffd14(u32 arg0, u32 arg1) {
    s32 temp_r2;
    u32 temp_r0;
    u32 var_r6;
    u8 temp_r1;

    var_r6 = 0;
    do {
        temp_r2 = (var_r6 * 0x54) + (s32) &native_arm7_data_03807ee0;
        temp_r1 = M2C_FIELD(temp_r2, u8 *, 3);
        if ((((u32) (temp_r1 << 0x1F) >> 0x1F) != 0) && (M2C_FIELD(temp_r2, u8 *, 1) == 0)) {
            temp_r0 = M2C_FIELD(temp_r2, u32 *, 0x44);
            if ((arg0 <= temp_r0) && (temp_r0 <= arg1)) {
                M2C_FIELD(temp_r2, u8 *, 3) = (u8) (temp_r1 & ~2);
                native_arm7_fn_037fea20(var_r6, 0U);
            }
        }
        var_r6 = (u32) (u8) (var_r6 + 1);
    } while (var_r6 < 0x10U);
}
