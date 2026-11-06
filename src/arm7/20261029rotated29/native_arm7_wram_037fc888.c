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
#define NULL ((void *)0)
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_arm7_fn_037fdd00(void);
extern u32 native_arm7_fn_037fc9a4(u32, u32);
extern u32 native_arm7_fn_037fc290(u32);
extern u32 native_arm7_fn_037fdd14(u32);
extern u8 native_arm7_data_03807714;
u32 native_arm7_wram_037fc888(void *arg0) {
    u32 temp_r0;
    u32 temp_r4;
    u32 temp_r7;

    temp_r4 = native_arm7_fn_037fdd00();
    temp_r7 = M2C_FIELD((u32) &native_arm7_data_03807714, u32 *, 4);
loop_1:
    temp_r0 = M2C_FIELD(arg0, u32 *, 8);
    if (temp_r0 == 0) {
        M2C_FIELD(arg0, u32 *, 8) = temp_r7;
        M2C_FIELD(arg0, s32 *, 0xC) = (s32) (M2C_FIELD(arg0, s32 *, 0xC) + 1);
        native_arm7_fn_037fc9a4(temp_r7, (u32) arg0);
    } else if (temp_r0 == temp_r7) {
        M2C_FIELD(arg0, s32 *, 0xC) = (s32) (M2C_FIELD(arg0, s32 *, 0xC) + 1);
    } else {
        M2C_FIELD(temp_r7, void **, 0x68) = arg0;
        native_arm7_fn_037fc290((u32) arg0);
        M2C_FIELD(temp_r7, void **, 0x68) = NULL;
        goto loop_1;
    }
    return native_arm7_fn_037fdd14(temp_r4);
}
