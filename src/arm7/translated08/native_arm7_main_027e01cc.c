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
extern u32 native_arm7_fn_037fc6d4(u32, u32, u32);
extern u32 native_arm7_fn_037fc760(u32, u32, u32);
extern u32 native_arm7_fn_038073f0(void);
extern u32 native_arm7_fn_038073a4(u32);
extern u32 native_arm7_fn_037fe708(void);
extern u32 native_arm7_fn_037fde70(void);
extern u32 native_arm7_data_027f7884;
extern u32 native_arm7_data_027f78dc;
u32 native_arm7_main_027e01cc(u32 arg0) {
    void *sp0;
    void *temp_r0;

    native_arm7_fn_037fc6d4((u32) &native_arm7_data_027f7884, arg0, 1U);
    native_arm7_fn_037fc760((u32) &native_arm7_data_027f78dc, (u32) &sp0, 1U);
    if (M2C_FIELD((sp0 + (M2C_FIELD(sp0, u16 *, 0xE) * 2)), u16 *, 0x14) == 0xE) {
        temp_r0 = (void *) native_arm7_fn_038073f0();
        M2C_FIELD(temp_r0, s16 *, 0) = 0x80;
        M2C_FIELD(temp_r0, s16 *, 2) = 0x13;
        M2C_FIELD(temp_r0, s16 *, 4) = 0x18;
        native_arm7_fn_038073a4((u32) temp_r0);
        native_arm7_fn_037fe708();
        native_arm7_fn_037fde70();
    }
    return (u32) sp0;
}
