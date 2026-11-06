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
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_02006b7c();
extern u32 native_fn_02090734();
extern u32 native_fn_ov006_021eee44();
extern u32 native_fn_ov006_021ef0a0();
extern u8 native_data_ov006_0221aad0[];
u32 native_ov006_021ef334(void) {
    u32 var_r0_2;
    u8 *var_r0;
    s32 var_r5;

    var_r5 = 1;
    if (M2C_FIELD(native_data_ov006_0221aad0, s32 *, 0x20) != 0) {
        if (native_fn_ov006_021eee44() != 0) {
            do {
                native_fn_02006b7c(0xA);
                var_r0_2 = native_fn_ov006_021ef0a0();
                if (var_r0_2 != 0) {
                    do {
                        switch (var_r0_2) {
                        case 4:
                        case 5:
                            break;
                        case 14:
                            var_r5 = 0;
                            break;
                        default:
                            var_r5 = 0;
                            break;
                        }
                        var_r0_2 = native_fn_ov006_021ef0a0();
                    } while (var_r0_2 != 0);
                }
            } while (var_r5 != 0);
        }
        M2C_FIELD(native_data_ov006_0221aad0, s32 *, 0x20) = 0;
    }
    var_r0 = native_data_ov006_0221aad0;
    if (M2C_FIELD(native_data_ov006_0221aad0, s32 *, 0x24) != 0) {
        M2C_FIELD(native_data_ov006_0221aad0, s32 *, 0x24) = 0;
        var_r0 = (u8 *) native_fn_02090734();
    }
    return (u32) var_r0;
}
