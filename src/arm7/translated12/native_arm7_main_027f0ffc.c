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
extern u32 native_arm7_fn_037f8a80(u32);
extern u32 native_arm7_fn_027ebbe0(u32);
extern u32 native_arm7_fn_027efec8(u32, u32);
extern u32 native_arm7_data_0380fff4;
void native_arm7_main_027f0ffc(s32 arg0, s32 arg1) {
    u32 var_r6;
    u32 temp_r7;
    s32 temp_r8;

    temp_r8 = arg0 * 0xC;
    var_r6 = M2C_FIELD((native_arm7_data_0380fff4 + temp_r8), u32 *, 0x194);
    if (var_r6 != -1U) {
        do {
            temp_r7 = native_arm7_fn_037f8a80(var_r6);
            if (arg0 != 2) {
                native_arm7_fn_027ebbe0(var_r6 + 0x10);
            }
            M2C_FIELD(var_r6, s16 *, 0x18) = 2;
            if (arg1 != 0) {
                native_arm7_fn_027efec8(native_arm7_data_0380fff4 + 0x194 + temp_r8, var_r6);
            }
            var_r6 = temp_r7;
        } while (temp_r7 != -1U);
    }
}
