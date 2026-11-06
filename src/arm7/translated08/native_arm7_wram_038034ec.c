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
extern u32 native_arm7_fn_037fe2b4(void);
extern u32 native_arm7_fn_037fe3ec(u32, u32);
extern u32 native_arm7_fn_037fe39c(u32, u32);
extern u32 native_arm7_fn_03803544(u32, u32);
extern u32 native_arm7_data_03809920;
u32 native_arm7_wram_038034ec(void) {
    u32 *var_r0;

    var_r0 = &native_arm7_data_03809920;
    if (M2C_FIELD(&native_arm7_data_03809920, s32 *, 8) == 0) {
        M2C_FIELD(&native_arm7_data_03809920, s32 *, 8) = 1;
        native_arm7_fn_037fe2b4();
        do {

        } while (native_arm7_fn_037fe3ec(0xEU, 0U) == 0);
        var_r0 = (u32 *) native_arm7_fn_037fe39c(0xEU, (u32) native_arm7_fn_03803544);
    }
    return (u32) var_r0;
}
