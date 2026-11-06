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
extern u32 native_fn_02040820();
extern u32 native_fn_0205d5bc();
extern u32 native_fn_ov000_021d84c4();
extern u32 native_fn_ov000_021da2a0();
extern u32 native_fn_ov000_021dff00();
extern u32 native_fn_ov000_021e1c34();
extern u32 native_fn_ov000_021e8850();
extern u32 native_fn_ov000_02210818();
extern u32 native_fn_ov000_02211e08();
extern u32 native_fn_ov000_02213758();
void native_main_02040434(void) {
    native_fn_ov000_021dff00();
    native_fn_ov000_021d84c4();
    native_fn_ov000_021da2a0();
    native_fn_ov000_021e1c34();
    native_fn_ov000_021e8850();
    native_fn_ov000_02210818();
    native_fn_ov000_02213758();
    native_fn_ov000_02211e08(0);
    native_fn_0205d5bc();
    native_fn_02040820();
}
