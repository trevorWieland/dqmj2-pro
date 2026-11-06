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
extern u32 native_arm7_fn_037fd5c0(u32);
extern u8 native_arm7_data_03808e60;
u32 native_arm7_wram_03801e68(u32 arg0) {
    u32 var_r0;
    void *temp_r4;

    var_r0 = arg0;
    temp_r4 = &native_arm7_data_03808e60 + (var_r0 << 6);
    if (*(&native_arm7_data_03808e60 + (var_r0 << 6)) != 0) {
        native_arm7_fn_037fd5c0((u32) (temp_r4 + 0x14));
        var_r0 = 0;
        M2C_FIELD(temp_r4, u8 *, 1) = (u8) (M2C_FIELD(temp_r4, u8 *, 1) + 1);
        M2C_FIELD(temp_r4, s8 *, 0) = 0;
    }
    return var_r0;
}
