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
extern u32 native_fn_020443c4();
extern u32 native_fn_020443d4();
extern u32 native_fn_0205be34();
extern u32 native_fn_0205be4c();
extern u32 native_fn_0205be74();
extern u32 native_fn_0205bea4();
extern u32 native_fn_0205bed4();
extern u32 native_fn_0205bf2c();
extern u32 native_fn_ov000_021d8a44();
extern u32 native_fn_ov000_021e07b8();
extern u32 native_fn_ov000_021e07d4();
extern u32 native_fn_ov000_0222b708();
extern u32 native_fn_ov000_0222b7b4();
extern u8 native_data_020f6054[];
u32 native_main_0203fc80(void) {
    native_fn_0205be34(M2C_FIELD(native_data_020f6054, u8 *, 0xC));
    native_fn_ov000_021e07b8(0);
    native_fn_0205be74();
    native_fn_0205bea4(M2C_FIELD((void *) native_fn_ov000_021e07d4(0), s32 *, 4));
    native_fn_0205bed4(M2C_FIELD((void *) native_fn_ov000_021d8a44(), s32 *, 0x4C));
    native_fn_0205be4c(-1);
    native_fn_0205bf2c(1);
    native_fn_020443c4(1);
    native_fn_020443d4(7);
    native_fn_ov000_0222b708();
    native_fn_ov000_0222b7b4();
    return 2U;
}
