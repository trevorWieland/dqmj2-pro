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
extern u32 native_fn_020273d8();
extern u32 native_fn_0205bf4c();
extern u32 native_fn_02066e4c();
extern u32 native_fn_02067340();
extern u32 native_fn_02067368();
extern u32 native_fn_020c40f4();
extern u32 native_fn_020c5678();
extern u32 native_fn_020c57bc();
extern u32 native_fn_ov000_021d8a28();
extern u32 native_fn_ov000_021d8ccc();
extern u32 native_fn_ov000_021da08c();
extern u32 native_fn_ov000_021df488();
extern u32 native_fn_ov000_021e07f0();
extern u32 native_fn_ov000_021e2eb0();
extern u32 native_fn_ov000_021e7390();
extern u32 native_fn_ov000_021e7cd0();
extern u32 native_fn_ov000_021e7d64();
extern u32 native_fn_ov000_0220a084();
extern u32 native_fn_ov000_0220a4b4();
extern u32 native_fn_ov000_02211530();
extern u32 native_fn_ov000_02211830();
extern u32 native_fn_ov000_02212f38();
extern u32 native_fn_ov000_022130d0();
extern u32 native_fn_ov000_02219d8c();
extern u8 native_data_020f6054[];
u32 native_main_0203dc44(void) {
    if ((M2C_FIELD(native_data_020f6054, u8 *, 0) == 0) && (M2C_FIELD(native_data_020f6054, u8 *, 0x29) == 0)) {
        native_fn_020273d8(1);
    }
    native_fn_02066e4c();
    native_fn_020c57bc();
    native_fn_020c5678();
    native_fn_ov000_021df488();
    native_fn_ov000_0220a084();
    native_fn_ov000_021e7cd0();
    native_fn_ov000_02211530();
    native_fn_ov000_02212f38();
    native_fn_ov000_021e7d64();
    native_fn_ov000_0220a4b4();
    native_fn_ov000_02211830();
    native_fn_ov000_022130d0();
    native_fn_ov000_021e7390();
    native_fn_ov000_021e2eb0();
    native_fn_ov000_021d8a28();
    native_fn_0205bf4c();
    native_fn_ov000_021da08c();
    native_fn_ov000_021d8ccc(0, 0, 0);
    if (M2C_FIELD(native_data_020f6054, u8 *, 0) != 0) {
        native_fn_02067340(0);
        native_fn_02067368();
        native_fn_ov000_021e07f0(2);
        native_fn_020c40f4(5);
        native_fn_ov000_02219d8c(0);
        M2C_FIELD(native_data_020f6054, u8 *, 0) = 0;
        M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 0x25;
    } else if (M2C_FIELD(native_data_020f6054, u8 *, 0x29) == 0) {
        M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 3;
    } else {
        native_fn_02067340(3);
        native_fn_02067368();
        native_fn_ov000_02219d8c(0);
        M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 0x25;
    }
    return 1U;
}
