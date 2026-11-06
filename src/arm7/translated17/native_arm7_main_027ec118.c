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
extern u32 native_arm7_fn_027ebfec(u32);
extern u32 native_arm7_fn_037fb928(u32);
extern u32 native_arm7_fn_027ead5c(u32);
extern u32 native_arm7_fn_027ead30(u32, u32);
extern u32 native_arm7_fn_027ec0d8(u32);
extern u32 native_arm7_fn_037fb8f0(u32);
extern u32 native_arm7_data_0380fff4;
extern u8 native_arm7_data_0480425c;
u32 native_arm7_main_027ec118(u32 arg0) {
    u32 temp_r0;
    u32 var_r0;
    u32 temp_r4;
    void *temp_r6;
    void *temp_r6_2;

    var_r0 = native_arm7_fn_027ebfec(arg0);
    if (var_r0 == 0x40) {
        var_r0 = (u32) M2C_FIELD(native_arm7_data_0380fff4, u16 *, 0x534);
        if (!(var_r0 & (1 << arg0))) {
            temp_r6 = M2C_FIELD(native_arm7_data_0380fff4, u16 *, 0x3D8) + (u32) &native_arm7_data_0480425c;
            temp_r4 = native_arm7_fn_037fb928(0x01000000U);
            if (arg0 == 0) {
                native_arm7_fn_027ead30((u32) (temp_r6 + 4), (u32) (u8) (native_arm7_fn_027ead5c((u32) (temp_r6 + 4)) | 1));
            } else {
                temp_r0 = native_arm7_fn_027ec0d8(arg0);
                temp_r6_2 = temp_r6 + 5 + (temp_r0 >> 3);
                native_arm7_fn_027ead30((u32) temp_r6_2, (u32) (u8) (native_arm7_fn_027ead5c((u32) temp_r6_2) | (1 << (temp_r0 & 7))));
            }
            var_r0 = native_arm7_fn_037fb8f0(temp_r4);
        }
    }
    return var_r0;
}
