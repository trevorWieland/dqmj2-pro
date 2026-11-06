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
extern u32 native_arm7_fn_037fd898(u32, u32, u32, u32, u32);
extern u32 native_arm7_fn_027e609c(void);
extern u32 native_arm7_fn_027e5f98(void);
extern u8 native_arm7_data_027f8884;
extern u8 native_arm7_data_0380b4bc;
u32 native_arm7_main_027e6050(void) {
    u32 var_r0;

    var_r0 = M2C_FIELD(M2C_FIELD((u32) &native_arm7_data_027f8884, void **, 0x550), u32 *, 0xC);
    if (var_r0 == 1) {
        native_arm7_fn_037fd898((u32) (u32) &native_arm7_data_0380b4bc, 0xCBU, 0x107U, (u32) native_arm7_fn_027e5f98, 3U);
        var_r0 = native_arm7_fn_027e609c();
    }
    return var_r0;
}
