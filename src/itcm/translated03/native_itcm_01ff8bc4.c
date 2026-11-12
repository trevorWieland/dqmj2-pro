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
extern u32 native_fn_02083504();
extern u32 native_fn_020844d0();
extern u32 ov000_context_02246600_02223c54();
u32 native_itcm_01ff8bc4(void) {
    s32 var_r5;
    u32 var_r6;
    void *temp_r0;

    var_r6 = 0;
    if (native_fn_02083504() == 2) {
        var_r5 = 0;
        do {
            temp_r0 = (void *) native_fn_020844d0(var_r5);
            if (M2C_FIELD(temp_r0, u8 *, 0xC0) != 0) {
                if ((M2C_FIELD(temp_r0, u16 *, 0x6C) == 0x10) && (M2C_FIELD(temp_r0, u16 *, 0x6E) == 1)) {
                    if (M2C_FIELD((void *) ov000_context_02246600_02223c54(), s8 *, 0x59) == 1) {
                        M2C_FIELD(temp_r0, u8 *, 0xC0) = 0U;
                    }
                }
                var_r6 += 1;
                M2C_FIELD(temp_r0, u16 *, 0xC2) = (u16) (M2C_FIELD(temp_r0, u16 *, 0xC2) - 1);
                if (M2C_FIELD(temp_r0, u16 *, 0xC2) == 0) {
                    M2C_FIELD(temp_r0, u8 *, 0xC0) = 0U;
                }
            }
            var_r5 += 1;
        } while (var_r5 < 3);
    }
    return var_r6;
}
