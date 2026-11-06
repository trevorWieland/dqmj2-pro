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
extern u32 native_arm7_fn_037fc6ac(u32, u32, u32);
extern u32 native_arm7_fn_037fe39c(u32, u32);
extern u32 native_arm7_fn_038025cc(u32, u32);
extern u32 native_arm7_data_03809060;
extern u32 native_arm7_data_03809080;
extern u32 native_arm7_data_03807edc;
u32 native_arm7_wram_03801ed8(void) {
    native_arm7_fn_037fc6ac((u32) &native_arm7_data_03809060, (u32) &native_arm7_data_03809080, 8U);
    native_arm7_fn_037fe39c(7U, (u32) native_arm7_fn_038025cc);
    native_arm7_data_03807edc = 0;
    return (u32) &native_arm7_data_03807edc;
}
