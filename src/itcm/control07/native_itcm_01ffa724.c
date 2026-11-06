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
extern u32 native_fn_01ffa02c();
extern u32 native_fn_01ffa824();
extern u32 native_fn_01ffa84c();
extern u32 native_fn_01ffb84c(s32);
extern u32 native_fn_020840a0();
extern u32 native_fn_020846bc();
extern u32 native_data_021cebe0;
u32 native_itcm_01ffa724(s32 arg0, s32 arg1) {
    s32 var_r5;
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r6;

    if (M2C_FIELD(&native_data_021cebe0, s32 *, 0x30) == 1) {
        return native_fn_01ffb84c(arg0);
    }
    temp_r6 = native_fn_020846bc();
    var_r5 = 0;
loop_3:
    if ((temp_r6 & (1 << var_r5)) && ((var_r5 == (u8) native_fn_01ffa824()) || (var_r5 == native_fn_01ffa84c())) && ((temp_r0_2 = native_fn_020840a0(var_r5), (temp_r0_2 == 0)) || (M2C_FIELD(temp_r0_2, u16 *, 2) != arg1) || (M2C_FIELD(temp_r0_2, u16 *, 0) != *(u16 *) native_fn_01ffa02c()))) {
        return 0U;
    }
    var_r5 += 1;
    if (var_r5 >= 8) {
        temp_r0 = native_fn_020840a0(arg0);
        if ((temp_r0 == 0) || (M2C_FIELD(temp_r0, u16 *, 2) != arg1) || (M2C_FIELD(temp_r0, u16 *, 0) != *(u16 *) native_fn_01ffa02c())) {
            return 0U;
        }
        return temp_r0 + 4;
    }
    goto loop_3;
}
