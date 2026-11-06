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
extern u32 native_arm7_fn_037fde70(void);
extern u32 native_arm7_data_0380b2c0;
u32 native_arm7_wram_0380660c(u32 arg0, s32 arg1) {
    if ((arg1 & 0x3F) == 1) {
        M2C_FIELD((u32) &native_arm7_data_0380b2c0, s32 *, 0x18) = arg1;
        M2C_FIELD((u32) &native_arm7_data_0380b2c0, s32 *, 0x28) = 1;
        return (u32) (u32) &native_arm7_data_0380b2c0;
    }
    return native_arm7_fn_037fde70();
}
