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
extern u32 native_fn_02045dc4();
extern u32 native_fn_0204bb08();
extern u32 native_fn_0204bb18();
extern u32 native_fn_0204bbd8();
extern u32 native_fn_02065818();
extern u8 native_data_020ddb08[];
extern u8 native_data_02102974[];
u32 native_main_0204bb28(s32 arg0) {
    s8 temp_r0_2;
    u32 temp_r0;
    u32 var_r4;

    var_r4 = 0;
    if ((arg0 >= 0) && (arg0 < 4)) {
        var_r4 = native_fn_0204bbd8();
        temp_r0_2 = M2C_FIELD(var_r4, s8 *, 8);
        if (temp_r0_2 == 0) {
            return (u32) temp_r0_2;
        }
    }
    if ((var_r4 != 0) && (native_fn_0204bb18() == 0)) {
        return native_fn_02065818((void *) var_r4, 0x1E, 0);
    }
    temp_r0 = native_fn_0204bb18();
    if (temp_r0 != 1) {
        return temp_r0;
    }
    native_fn_02045dc4(*native_data_02102974, *native_data_020ddb08, 0x1E, 0, 2, 2);
    return native_fn_0204bb08(2);
}
