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
extern u32 native_fn_0202824c();
extern u32 native_fn_0202a090();
extern u32 native_fn_0202a1e0();
extern u32 native_fn_0202a5ec();
extern u32 native_fn_020414b0();
extern u32 native_fn_020414c8();
extern u32 native_fn_02041898();
extern u32 native_fn_020430cc();
extern u32 native_fn_020430e4();
extern u32 native_fn_020431d4();
extern u32 native_fn_02043304();
extern u32 native_fn_0205f5dc();
extern u32 native_fn_020642dc();
extern u32 native_fn_020c225c();
extern u8 native_data_020f69c4[];
u32 native_main_020430f8(void) {
    s32 var_r4;

    var_r4 = 0x29800;
    if ((native_fn_020642dc() == 0x19) || (native_fn_020642dc() == 0x1A) || (native_fn_020642dc() == 0x1B)) {
        var_r4 = 0x19000;
    }
    native_fn_0202a090(1, 0xE4000);
    native_fn_0202a090(4, 0xC800);
    if (native_fn_0202a090(2, var_r4) == 0) {
        native_fn_0202a5ec();
        native_fn_020c225c((var_r4 * 0x10) | 0x90000002);
    }
    M2C_FIELD(native_data_020f69c4, s8 *, 2) = (s8) native_fn_0202a1e0(1);
    native_fn_0202824c(native_fn_020430cc, native_fn_020430e4);
    native_fn_020414b0(0x3F);
    native_fn_020414c8(0x3F);
    native_fn_02041898(2);
    native_fn_020431d4();
    native_fn_02043304();
    M2C_FIELD(native_data_020f69c4, u32 *, 8) = native_fn_0205f5dc();
    native_fn_020273d8(2);
    M2C_FIELD(native_data_020f69c4, s8 *, 5) = 0;
    M2C_FIELD(native_data_020f69c4, s8 *, 3) = 0;
    return (u32) native_data_020f69c4;
}
