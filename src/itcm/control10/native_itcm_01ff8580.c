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
extern u32 native_fn_02062a10(u32);
extern u32 native_fn_02062a68();
extern u32 native_fn_02062a78();
extern u32 native_data_01fff8a0;
void native_itcm_01ff8580(s32 arg0) {
    s32 var_r4;
    s32 var_r5;
    u32 temp_r0;
    u32 var_r0;

    var_r5 = (arg0 * 0x48) + (s32) &native_data_01fff8a0;
    var_r4 = 0;
    do {
        if (var_r4 < 3) {
            var_r0 = native_fn_02062a68(var_r4);
        } else {
            var_r0 = native_fn_02062a78(var_r4 - 3);
        }
        M2C_FIELD(var_r5, volatile u32 *, 0) = var_r0;
        if ((var_r0 = M2C_FIELD(var_r5, volatile u32 *, 0)) != 0) {
            temp_r0 = native_fn_02062a10(var_r0);
            if (temp_r0 != 0) {
                M2C_FIELD(var_r5, s16 *, 4) = (s16) M2C_FIELD(temp_r0, s16 *, 0x24);
                M2C_FIELD(var_r5, s16 *, 6) = (s16) M2C_FIELD(temp_r0, s16 *, 0x26);
                M2C_FIELD(var_r5, u8 *, 8) = (u8) M2C_FIELD(temp_r0, u8 *, 0x32);
                M2C_FIELD(var_r5, u8 *, 9) = (u8) M2C_FIELD(temp_r0, u8 *, 0x33);
            }
        }
        var_r4 += 1;
        var_r5 += 0xC;
    } while (var_r4 < 6);
}
