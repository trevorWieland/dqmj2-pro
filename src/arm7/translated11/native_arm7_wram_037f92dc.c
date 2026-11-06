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
extern u32 native_arm7_fn_037fa21c(void);
extern u32 native_arm7_fn_037fa328(void);
extern u32 native_arm7_fn_037f93b0(void);
extern u32 native_arm7_fn_037f943c(void);
extern u32 native_arm7_fn_037f96e0(void);
extern u32 native_arm7_fn_027eb83c(void);
extern u32 native_arm7_fn_037f977c(void);
extern u32 native_arm7_fn_037f988c(void);
extern u32 native_arm7_fn_037f9c70(void);
extern u32 native_arm7_fn_037f974c(void);
extern u32 native_arm7_fn_037f9a08(void);
extern u32 native_arm7_fn_037fa12c(u32);
extern u32 native_arm7_data_04808010;
extern u32 native_arm7_data_0380fff8;
u32 native_arm7_wram_037f92dc(void) {
    s32 temp_r6;
    u32 temp_r0;

loop_1:
    temp_r6 = M2C_FIELD((u32) &native_arm7_data_04808010, u16 *, 0) & M2C_FIELD((u32) &native_arm7_data_04808010, u16 *, 2);
    if (temp_r6 != 0) {
        if (temp_r6 & 0x80) {
            native_arm7_fn_037fa21c();
        }
        if (temp_r6 & 0x40) {
            native_arm7_fn_037fa328();
        }
        if (temp_r6 & 0x8000) {
            native_arm7_fn_037f93b0();
        }
        if (temp_r6 & 0x4000) {
            native_arm7_fn_037f943c();
        }
        if (temp_r6 & 0x2000) {
            native_arm7_fn_037f96e0();
        }
        if (temp_r6 & 0x800) {
            native_arm7_fn_027eb83c();
        }
        if (temp_r6 & 8) {
            native_arm7_fn_037f977c();
        }
        if (temp_r6 & 4) {
            native_arm7_fn_037f988c();
        }
        if (temp_r6 & 1) {
            native_arm7_fn_037f9c70();
        }
        if (temp_r6 & 0x30) {
            native_arm7_fn_037f974c();
        }
        if (temp_r6 & 2) {
            native_arm7_fn_037f9a08();
        }
        if (temp_r6 & 0x1000) {
            native_arm7_fn_037fa12c(1U);
        }
        goto loop_1;
    }
    temp_r0 = native_arm7_data_0380fff8 | 0x01000000;
    native_arm7_data_0380fff8 = temp_r0;
    return temp_r0;
}
