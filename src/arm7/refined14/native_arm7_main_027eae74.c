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
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_main_027eae74(void *arg0) {
    void *temp_lr;
    void *temp_r1;
    void *temp_r4;

    temp_r4 = M2C_FIELD(arg0, void **, 8);
    temp_lr = temp_r4 - 4;
    if ((M2C_FIELD(temp_r4, u16 *, -4) == 0xB6B8) && (M2C_FIELD(temp_lr, u16 *, 2) == 0x1D46)) {
        return 0U;
    }
    M2C_FIELD(temp_r4, s16 *, 0xA) = 1;
    M2C_FIELD(temp_lr, u16 *, 0) = 0xB6B8;
    M2C_FIELD(temp_lr, u16 *, 2) = 0x1D46U;
    temp_r1 = M2C_FIELD(arg0, void **, 8);
    M2C_FIELD(temp_r1, u16 *, 0xC) = 0xB6B8;
    M2C_FIELD(temp_r1, s16 *, 0xE) = 0x1D46;
    M2C_FIELD(native_arm7_data_0380fff4, u16 *, 0x3FA) = (u16) (M2C_FIELD(native_arm7_data_0380fff4, u16 *, 0x3FA) + 1);
    return 1U;
}
