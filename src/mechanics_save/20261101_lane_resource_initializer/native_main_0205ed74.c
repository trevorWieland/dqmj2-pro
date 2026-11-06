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
extern u32 native_fn_02008d78(void *, u32, u32);
extern u32 native_fn_02037a50(u32, u32);
extern u32 native_fn_02037ad8(u32);
extern u32 native_fn_02037dc8(void);
extern u32 native_fn_020380f4(void *);
extern u32 native_fn_02038a34(void *, u32, u32, u32);
extern u32 native_fn_02039a14(u32);
extern u32 native_fn_02039d60(u32, u32);
extern u32 native_fn_0203a06c(void *);
extern u32 native_fn_0205ed58(u32);
typedef struct {
    u8 field_0;
    s8 field_1;
    u8 unknown_2[0x2];
    u32 field_4;
    s32 field_8;
    s32 field_c;
} Record_native_data_021b8ae0;
extern Record_native_data_021b8ae0 native_data_021b8ae0;
extern u8 native_data_021b8af0[];
extern u8 native_data_021b8b10[];
extern u8 native_data_021b8b90[];
u32 native_main_0205ed74(s32 arg0, s32 arg1, s32 arg2, s32 arg3) {
    u32 temp_r0;
    s32 var_r6;
    u8 *var_r6_2;
    u32 var_r7;
    s32 var_r8_2;
    u8 *var_r8;

    native_data_021b8ae0.field_1 = 0;
    native_fn_02037dc8();
    native_data_021b8ae0.field_4 = 0U;
    native_data_021b8ae0.field_8 = 0;
    native_data_021b8ae0.field_c = 0;
    native_fn_02008d78(native_data_021b8b90, 0, 0x94);
    if ((arg0 != 0) && (arg1 != 0)) {
        temp_r0 = native_fn_02037a50(arg0, arg1);
        native_data_021b8ae0.field_4 = temp_r0;
        if (temp_r0 != 0) {
            native_fn_02037ad8(temp_r0);
            native_data_021b8ae0.field_8 = arg0;
            native_data_021b8ae0.field_c = arg1;
            if (arg2 != 0) {
                if (native_fn_02038a34(native_data_021b8b90, arg2, native_data_021b8ae0.field_4, 0) != 0) {
                    if (native_fn_02039a14(native_data_021b8ae0.field_4) != 0) {
                        if (arg3 >= 0) {
                            native_fn_02039d60(arg3, native_data_021b8ae0.field_4);
                            var_r7 = native_fn_0205ed58(0);
                        } else {
                            var_r7 = native_fn_0205ed58(0);
                        }
                    } else {
                        var_r7 = native_fn_0205ed58(1);
                    }
                } else {
                    var_r7 = native_fn_0205ed58(2);
                }
            } else {
                var_r7 = native_fn_0205ed58(0);
            }
        } else {
            var_r7 = native_fn_0205ed58(3);
        }
    } else {
        var_r7 = native_fn_0205ed58(0);
    }
    if (var_r7 != 0) {
        var_r8 = native_data_021b8b10;
        var_r6 = 0;
        do {
            native_fn_020380f4(var_r8);
            M2C_FIELD((native_data_021b8b10 + (var_r6 * 8)), s16 *, 4) = -1;
            var_r6 += 1;
            M2C_FIELD(var_r8, u8 *, 7) &= ~1U;
            M2C_FIELD(var_r8, u8 *, 7) &= ~2U;
            var_r8 += 8;
        } while (var_r6 < 0x10);
        var_r6_2 = native_data_021b8af0;
        var_r8_2 = 0;
        do {
            native_fn_0203a06c(var_r6_2);
            M2C_FIELD((native_data_021b8af0 + (var_r8_2 * 8)), s16 *, 4) = -1;
            var_r8_2 += 1;
            M2C_FIELD(var_r6_2, u8 *, 7) &= ~1U;
            M2C_FIELD(var_r6_2, u8 *, 7) &= ~2U;
            var_r6_2 += 8;
        } while (var_r8_2 < 4);
        native_data_021b8ae0.field_0 = 0x7F;
    }
    return var_r7;
}
