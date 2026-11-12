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
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
extern u32 native_fn_02046af4();
extern u32 native_fn_02049ad0();
extern u32 native_fn_02049f14();
extern u32 native_fn_02049f24();
extern u32 native_fn_02049f30();
extern u32 ov000_display_context_02215698();
extern u32 native_fn_ov000_02217bdc();
extern u32 native_fn_ov000_02217cf0();
extern u8 native_data_021c6638[];
extern u8 native_data_021c9698[];
u32 native_main_0207969c(void) {
    u32 temp_r4;
    u32 temp_r5;
    void *temp_r2;

    temp_r5 = ov000_display_context_02215698();
    temp_r4 = native_fn_02049f24();
    native_fn_02049f30();
    temp_r2 = M2C_FIELD(*(void **) native_fn_02049ad0((s8) (*(u32 *)native_data_021c6638 + 5)), void **, 4);
    native_fn_02046af4(native_data_021c9698, M2C_FIELD(temp_r2, s32 *, 0x68), M2C_FIELD(temp_r2, u8 *, 0x5E), 0, temp_r4, 0xFF);
    native_fn_02049f14(temp_r4);
    native_fn_ov000_02217bdc(0, 1, 5, 1, 1, -1);
    native_fn_ov000_02217cf0(temp_r5 + 0x10);
    return 0U;
}
