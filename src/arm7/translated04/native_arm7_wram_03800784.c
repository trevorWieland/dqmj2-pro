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
extern u32 native_arm7_data_03807ec0;
u32 native_arm7_wram_03800784(s32 arg0) {
    s32 temp_r2;
    u32 temp_r0;

    temp_r2 = arg0 & ~3;
    M2C_FIELD(&native_arm7_data_03807ec0, s32 *, 4) = temp_r2;
    M2C_FIELD(&native_arm7_data_03807ec0, s32 *, 8) = (s32) (temp_r2 + 0x10);
    M2C_FIELD(&native_arm7_data_03807ec0, s32 *, 0xC) = (s32) M2C_FIELD(temp_r2, s32 *, 0);
    M2C_FIELD(&native_arm7_data_03807ec0, s32 *, 0x10) = (s32) M2C_FIELD(temp_r2, s32 *, 4);
    M2C_FIELD(&native_arm7_data_03807ec0, s32 *, 0x14) = (s32) M2C_FIELD(temp_r2, s32 *, 8);
    temp_r0 = M2C_FIELD(temp_r2, u32 *, 0xC);
    M2C_FIELD(&native_arm7_data_03807ec0, u32 *, 0x18) = temp_r0;
    return temp_r0;
}
