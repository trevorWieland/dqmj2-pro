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
extern u32 native_fn_0202a164();
extern u32 native_fn_0202a1e0();
extern u32 native_fn_0203d0fc();
extern u32 native_fn_0205d634();
extern u32 native_fn_ov000_021df488();
extern u32 native_fn_ov000_021e6394();
extern u32 native_fn_ov000_021e64c4();
extern u32 native_fn_ov000_021e76d8();
extern u32 native_fn_ov000_021e7734();
extern u32 native_fn_ov000_021f3b28();
extern u32 native_fn_ov000_0222194c();
extern u32 native_fn_ov000_0222a494();
extern u8 native_data_02106950[];
u32 native_main_0205e368(void) {
    native_fn_0205d634();
    native_fn_ov000_021e7734();
    native_fn_ov000_021f3b28();
    native_fn_ov000_021e64c4();
    native_fn_ov000_021e76d8();
    native_fn_ov000_0222194c();
    native_fn_ov000_021df488();
    native_fn_ov000_021e6394();
    if (native_fn_0203d0fc() != 0) {
        native_fn_ov000_0222a494();
    }
    native_fn_0202a1e0((s8) *native_data_02106950);
    native_fn_0202a164(1);
    return native_fn_0202a164(2);
}
