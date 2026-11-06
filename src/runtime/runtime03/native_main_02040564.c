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
extern u32 native_fn_02040494();
extern u32 native_fn_020404f0();
extern u32 native_fn_020406a8();
extern u32 native_fn_020406b8();
extern u32 native_fn_020406c8();
extern u32 native_fn_020612ec();
extern u32 native_fn_02062074();
extern u32 native_fn_02067340();
extern u32 native_fn_ov000_021e7b9c();
u32 native_main_02040564(void) {
    u32 var_r4;

    var_r4 = 0;
    if (native_fn_020406b8() == 0) {
        native_fn_020406a8(1);
        native_fn_020404f0(0x32);
        native_fn_02040494();
        native_fn_02067340(2);
        native_fn_020612ec(0, 0, 0x6000, 0);
        native_fn_02062074(0);
        native_fn_020406c8(0);
        native_fn_ov000_021e7b9c(0x52);
        var_r4 = 1;
    }
    return var_r4;
}
