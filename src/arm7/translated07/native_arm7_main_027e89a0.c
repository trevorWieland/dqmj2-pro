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
extern u32 native_arm7_fn_027eabec(void);
extern u32 native_arm7_fn_027e9d00(void);
extern u32 native_arm7_fn_027ea72c(void);
extern u32 native_arm7_fn_027e8d50(void);
extern u32 native_arm7_fn_027e8bd0(void);
extern u32 native_arm7_fn_027e8de8(u32, u32);
extern u32 native_arm7_fn_027ec6f0(void);
extern u32 native_arm7_fn_027ee0bc(void);
extern u32 native_arm7_fn_027ec480(void);
extern u32 native_arm7_fn_027e97bc(void);
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_main_027e89a0(void) {
    native_arm7_fn_027eabec();
    native_arm7_fn_027e9d00();
    native_arm7_fn_027ea72c();
    native_arm7_fn_027e8d50();
    native_arm7_fn_027e8bd0();
    native_arm7_fn_027e8de8(M2C_FIELD(native_arm7_data_0380fff4, u32 *, 0x31C), (u32) M2C_FIELD(native_arm7_data_0380fff4, u16 *, 0x320));
    native_arm7_fn_027ec6f0();
    native_arm7_fn_027ee0bc();
    native_arm7_fn_027ec480();
    return native_arm7_fn_027e97bc();
}
