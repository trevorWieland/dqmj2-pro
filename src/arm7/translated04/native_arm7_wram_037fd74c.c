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
extern u32 native_arm7_fn_037fb928(u32);
extern u32 native_arm7_data_038078b4;
void native_arm7_wram_037fd74c(void) {
    if (M2C_FIELD(&native_arm7_data_038078b4, u16 *, 0) == 0) {
        M2C_FIELD(&native_arm7_data_038078b4, u16 *, 0) = 1U;
        M2C_FIELD(&native_arm7_data_038078b4, s32 *, 0xC) = 0;
        M2C_FIELD(&native_arm7_data_038078b4, s32 *, 0x10) = 0;
        native_arm7_fn_037fb928(4U);
        M2C_FIELD(&native_arm7_data_038078b4, s32 *, 8) = 0;
        M2C_FIELD(&native_arm7_data_038078b4, s32 *, 4) = 0;
    }
}
