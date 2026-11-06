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
extern u32 native_arm7_fn_027eaef4(void);
extern u32 native_arm7_fn_027f0120(u32, u32);
extern u32 native_arm7_data_0380fff4;
void native_arm7_main_027eaf30(void *arg0) {
    if (M2C_FIELD(arg0, u16 *, 0) != 0) {
        native_arm7_fn_027eaef4();
        native_arm7_fn_027f0120(M2C_FIELD(arg0, u32 *, 8), M2C_FIELD(arg0, s32 *, 0xC) - 0x10);
        M2C_FIELD(native_arm7_data_0380fff4, u16 *, 0x3FC) = (u16) (M2C_FIELD(native_arm7_data_0380fff4, u16 *, 0x3FC) + 1);
    }
}
