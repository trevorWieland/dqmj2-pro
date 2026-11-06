typedef unsigned char u8;
typedef signed char s8;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern void native_fn_02068bd4(u32);
extern u32 native_fn_02068c14(u32,u32,u32,u32);
extern u32 native_fn_02069330(void *,s32,s32,s32,u8,u8,u8,s32);
extern void native_fn_020bfb10(s32);
extern void native_fn_020bfe70(u32);
extern void native_fn_020c01f0(void);
extern u32 native_fn_020c956c(void);
extern u32 native_fn_020c957c(u32);
extern void *native_fn_ov000_02223d40(s32,s32);
#define M2C_FIELD(value,type,offset) (*(type)((s8 *)(value)+(offset)))
u32 native_main_020c966c(void) {
    u32 var_r9_2;
    s8 var_r10_2;
    s8 var_r9;
    void *temp_r0;
    void *temp_r0_2;
    u32 var_r10;

    native_fn_02068bd4(native_fn_020c956c());
    var_r10 = 0;
    var_r9 = 0;
    do {
        temp_r0 = native_fn_ov000_02223d40(0, var_r9);
        if ((temp_r0 != 0) && (M2C_FIELD(temp_r0, s16 *, 0x18) != 0)) {
            native_fn_02069330((void *) temp_r0, 0, 0, (s32)(u8) var_r10, 0U, 0xCU, 0xFU, 1);
            var_r10 += 1;
        }
        var_r9 += 1;
    } while ((s32) var_r9 < 3);
    var_r9_2 = 0;
    var_r10_2 = 0;
    do {
        temp_r0_2 = native_fn_ov000_02223d40(1, var_r10_2);
        if ((temp_r0_2 != 0) && (M2C_FIELD(temp_r0_2, s16 *, 0x18) != 0)) {
            native_fn_02069330((void *) temp_r0_2, 1, 0, (s32)(u8) var_r9_2, 0U, 0xCU, 0xFU, 1);
            var_r9_2 += 1;
        }
        var_r10_2 += 1;
    } while ((s32) var_r10_2 < 3);
    native_fn_02068c14(2, 0x24, 0x20, 1);
    return native_fn_020c957c(1U);
}
