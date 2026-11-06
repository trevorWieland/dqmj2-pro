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
extern u32 native_fn_0205d53c();
extern u32 native_fn_ov000_021d8958();
extern u32 native_fn_ov000_021da16c();
extern u32 native_fn_ov000_021e0764();
extern u32 native_fn_ov000_02211960();
extern u32 native_fn_ov000_0221310c();
extern u32 native_fn_ov000_02219e04();
void native_main_0203dd48(void) {
    native_fn_ov000_02219e04();
    native_fn_ov000_021d8958();
    native_fn_ov000_021e0764();
    native_fn_0205d53c();
    native_fn_ov000_0221310c();
    native_fn_ov000_02211960(0);
    native_fn_ov000_021da16c();
}
