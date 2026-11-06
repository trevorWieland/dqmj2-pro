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
extern u32 native_fn_02062850();
extern u32 native_fn_020628b0();
extern u32 native_fn_02062904();
extern u32 native_fn_02062980();
extern u32 native_fn_02062a10();
extern u8 native_data_01fff8a0[];
u8 native_data_01fff8a0[0x90];

u32 native_itcm_01ff8604(s32 arg0) {
    s32 var_r4;
    s32 var_r5;
    s32 var_r6;
    s32 var_r6_2;
    u32 var_r0;

    var_r6 = 0;
    do {
        native_fn_020628b0(0);
        var_r6 += 1;
    } while (var_r6 < 3);
    var_r6_2 = 0;
    do {
        native_fn_02062980(0);
        var_r6_2 += 1;
    } while (var_r6_2 < 3);
    var_r5 = (arg0 * 0x48) + (s32) native_data_01fff8a0;
    var_r4 = 0;
    do {
        var_r0 = M2C_FIELD(var_r5, u32 *, 0);
        if (var_r0 != 0) {
            if (var_r4 < 3) {
                native_fn_02062850();
            } else {
                native_fn_02062904();
            }
            var_r0 = native_fn_02062a10(M2C_FIELD(var_r5, u32 *, 0));
            if (var_r0 != 0) {
                M2C_FIELD(var_r0, s16 *, 0x24) = (s16) M2C_FIELD(var_r5, s16 *, 4);
                M2C_FIELD(var_r0, s16 *, 0x26) = (s16) M2C_FIELD(var_r5, s16 *, 6);
                M2C_FIELD(var_r0, u8 *, 0x32) = (u8) M2C_FIELD(var_r5, u8 *, 8);
                M2C_FIELD(var_r0, u8 *, 0x33) = (u8) M2C_FIELD(var_r5, u8 *, 9);
            }
        }
        var_r4 += 1;
        var_r5 += 0xC;
    } while (var_r4 < 6);
    return var_r0;
}
