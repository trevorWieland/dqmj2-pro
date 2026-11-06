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
extern u32 native_fn_0202bb28();
extern u32 native_fn_0202bb88();
extern u32 native_fn_02037ad8();
extern u8 native_data_020f47b8[];
u32 native_main_020385c8(s32 arg0, void *arg1) {
    s32 temp_r5;
    u32 temp_r0;

    temp_r5 = (arg0 * 0x24) + (s32) native_data_020f47b8;
    temp_r0 = native_fn_0202bb88(temp_r5 + 0xC, 0);
    if (temp_r0 == 0) {
        return 0U;
    }
    native_fn_0202bb28(temp_r5 + 0xC, temp_r0);
    M2C_FIELD(temp_r0, void **, 0xC) = arg1;
    M2C_FIELD(arg1, u32 *, 8) = temp_r0;
    native_fn_02037ad8(M2C_FIELD(temp_r0, u32 *, 8));
    return M2C_FIELD(temp_r0, u32 *, 8);
}
