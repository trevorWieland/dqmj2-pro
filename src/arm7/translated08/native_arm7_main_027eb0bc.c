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
extern u32 native_arm7_fn_037f886c(u32, u32);
extern u32 native_arm7_fn_037fb928(u32);
extern u32 native_arm7_fn_037fb8f0(u32);
extern u32 native_arm7_fn_037f8d58(u32, u32);
extern u32 native_arm7_data_0380fff4;
void native_arm7_main_027eb0bc(void) {
    u32 temp_r0;
    u32 temp_r0_2;
    void *temp_r4;

    temp_r4 = native_arm7_data_0380fff4 + 0x344;
    if (M2C_FIELD(temp_r4, u16 *, 0xB0) != 0) {
        temp_r0 = native_arm7_fn_037f886c(native_arm7_data_0380fff4 + 0x188, 0x12U);
        if (temp_r0 != 0) {
            M2C_FIELD(temp_r0, s16 *, 0xC) = 0x186;
            M2C_FIELD(temp_r0, s16 *, 0xE) = 1;
            temp_r0_2 = native_arm7_fn_037fb928(0x01000000U);
            M2C_FIELD(temp_r0, u16 *, 0x10) = (u16) M2C_FIELD(temp_r4, u16 *, 0xB0);
            M2C_FIELD(temp_r4, u16 *, 0xB0) = 0U;
            native_arm7_fn_037fb8f0(temp_r0_2);
            native_arm7_fn_037f8d58(native_arm7_data_0380fff4 + 0x188, temp_r0);
        }
    }
}
