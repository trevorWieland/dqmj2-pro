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
extern u32 native_arm7_fn_037fe39c(u32, u32, u32, u32);
extern u32 native_arm7_fn_037fddc4(u32, u32, u32, u32);
extern u16 native_arm7_data_038078c8;
void native_arm7_wram_037fdd7c(void) {
    if (native_arm7_data_038078c8 == 0) {
        native_arm7_data_038078c8 = 1;
        native_arm7_fn_037fe39c(0xCU, (u32) native_arm7_fn_037fddc4, (u32) &native_arm7_data_038078c8, 1U);
    }
}
