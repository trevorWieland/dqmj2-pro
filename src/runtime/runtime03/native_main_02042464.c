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
extern u32 native_fn_02041268();
extern u32 native_fn_02041af0();
extern u32 native_fn_0204244c();
extern u32 native_fn_02042cb8();
extern u32 native_fn_02042fd4();
u32 native_main_02042464(void *arg0, s32 arg1, s32 arg2) {
    s8 var_r0;
    u32 var_r5;

    var_r5 = 0;
    if ((arg2 == 0) && (M2C_FIELD(arg0, s32 *, 0x164) == arg1)) {

    } else if (native_fn_02042fd4(arg1) != 0) {
        var_r5 = native_fn_02041268(arg0, native_fn_02041af0(arg1) + 4, 0, M2C_FIELD(arg0, u8 *, 0x15F));
        if (var_r5 != 0) {
            native_fn_0204244c(arg0);
            M2C_FIELD(arg0, s32 *, 0x164) = arg1;
            if (native_fn_02042cb8(arg1) & 1) {
                var_r0 = 1;
            } else {
                var_r0 = 0;
            }
            M2C_FIELD(arg0, s8 *, 0x1DE) = var_r0;
            M2C_FIELD(arg0, u8 *, 0x162) = (u8) (M2C_FIELD(arg0, u8 *, 0x162) | 1);
        }
    }
    return var_r5;
}
