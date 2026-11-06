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
extern u32 native_arm7_fn_037fd128(void);
extern u32 native_arm7_fn_037fd34c(void);
extern u32 native_arm7_fn_037fd3a0(u32);
extern u32 native_arm7_fn_03806108(void);
extern u32 native_arm7_fn_037fbbfc(void);
extern u32 native_arm7_fn_037fe2b4(void);
extern u32 native_arm7_fn_037fe39c(u32, u32);
extern u32 native_arm7_fn_03806498(void);
extern u32 native_arm7_fn_0380660c(u32, u32, u32);
extern u32 native_arm7_fn_0380663c(u32, u32);
extern u32 native_arm7_fn_038069b4(u32, u32);
extern u32 native_arm7_data_0380b2f0;
extern u32 native_arm7_data_0380b2c0;
extern u32 native_arm7_data_03806670;
u32 native_arm7_wram_038063f8(void) {
    u32 *var_r0;

    native_arm7_fn_037fd128();
    native_arm7_fn_037fd34c();
    native_arm7_fn_037fd3a0((u32) &native_arm7_data_0380b2f0);
    var_r0 = &native_arm7_data_0380b2c0;
    if (M2C_FIELD(&native_arm7_data_0380b2c0, s32 *, 0x14) == 0) {
        M2C_FIELD(&native_arm7_data_0380b2c0, s32 *, 0x14) = 1;
        native_arm7_fn_03806108();
        var_r0 = (u32 *) native_arm7_fn_037fbbfc();
        if (var_r0 != (u32 *)-3) {
            M2C_FIELD(&native_arm7_data_0380b2c0, s16 *, 0) = (s16) var_r0;
            native_arm7_fn_037fe2b4();
            native_arm7_fn_037fe39c(0xDU, (u32) native_arm7_fn_0380660c);
            native_arm7_fn_03806498();
            native_arm7_fn_037fe39c(0xDU, (u32) native_arm7_fn_0380663c);
            native_arm7_fn_037fe39c(0x10U, (u32) &native_arm7_data_03806670);
            var_r0 = (u32 *) native_arm7_fn_037fe39c(0x11U, (u32) native_arm7_fn_038069b4);
        }
    }
    return (u32) var_r0;
}
