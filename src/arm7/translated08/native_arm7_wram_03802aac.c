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
extern u32 native_arm7_fn_038027d0(void);
extern u32 native_arm7_fn_03802f04(u32);
extern u32 native_arm7_data_038090c0;
extern u32 native_arm7_data_038096c0;
void native_arm7_wram_03802aac(void) {
    u8 temp_r4;

    temp_r4 = M2C_FIELD(native_arm7_data_038090c0, u8 *, 0x54);
    if ((temp_r4 != 0xFF) && (native_arm7_data_038096c0 == 0)) {
        if (temp_r4 != native_arm7_fn_038027d0()) {
            native_arm7_fn_03802f04((u32) temp_r4);
        }
        native_arm7_data_038096c0 = 1;
    }
}
