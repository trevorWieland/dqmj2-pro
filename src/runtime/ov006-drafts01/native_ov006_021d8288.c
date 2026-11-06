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
extern u32 native_fn_02044cdc();
extern u32 native_fn_02062a50();
extern u32 native_fn_02062aa0();
extern u8 native_data_ov006_0220eba4[];
u32 native_ov006_021d8288(s32 arg0) {
    s32 temp_r0_3;
    u32 temp_r0;
    u32 temp_r0_2;
    u32 var_r0;
    u8 *var_r1;
    u8 *var_r1_2;
    s32 var_r2;
    s32 var_r4;
    s32 var_r5;

    var_r4 = 0;
    if (arg0 == 1) {
        var_r5 = 0;
        var_r0 = native_fn_02062aa0();
        if ((s32) var_r0 > 0) {
            do {
                temp_r0_3 = native_fn_02044cdc(M2C_FIELD((void *) native_fn_02062a50(var_r5), s16 *, 0x18)) + 1;
                var_r5 += 1;
                var_r4 += temp_r0_3;
                var_r0 = native_fn_02062aa0();
            } while (var_r5 < (s32) var_r0);
        }
        var_r2 = 0;
        if (var_r4 <= 0) {
            return var_r0;
        }
        var_r1 = native_data_ov006_0220eba4;
        do {
            var_r2 += 1;
            temp_r0_2 = M2C_FIELD(var_r1, u32 *, 0x7C) | 2;
            M2C_FIELD(var_r1, u32 *, 0x7C) = temp_r0_2;
            var_r1 += 0x90;
        } while (var_r2 < var_r4);
        return temp_r0_2;
    }
    var_r1_2 = native_data_ov006_0220eba4;
    do {
        var_r4 += 1;
        temp_r0 = M2C_FIELD(var_r1_2, u32 *, 0x7C) & ~2;
        M2C_FIELD(var_r1_2, u32 *, 0x7C) = temp_r0;
        var_r1_2 += 0x90;
    } while (var_r4 < 3);
    return temp_r0;
}
