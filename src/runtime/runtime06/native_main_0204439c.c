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
extern u32 native_fn_ov001_021d73c8();
extern u32 native_fn_ov001_021d8b34();
extern u32 native_fn_ov001_021d933c();
extern u32 native_fn_ov001_021db314();
extern u32 native_fn_ov001_021e349c();
extern u32 native_fn_ov001_021eef4c();
extern u32 native_fn_ov001_02217fc8();
void native_main_0204439c(void) {
    native_fn_ov001_021d933c();
    native_fn_ov001_021d73c8();
    native_fn_ov001_021d8b34();
    native_fn_ov001_021e349c();
    native_fn_ov001_02217fc8();
    native_fn_ov001_021db314();
    native_fn_ov001_021eef4c();
    native_fn_02040820();
}
