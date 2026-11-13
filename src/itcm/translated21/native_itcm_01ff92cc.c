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
extern u32 native_fn_01ffa440(void);
extern u32 native_fn_01ffa44c(u32);
extern u32 native_fn_01ffa484(u32);
extern u32 native_fn_01ffa5ac(u32, u32, u32);
extern u32 native_fn_01ffa804(void);
extern u32 native_fn_01ffac9c(u32, u32, u32, u32, u32, u32);
extern u32 native_fn_01ffae9c(u32, u32, u32, u32);
extern u32 native_fn_01ffb060(u32);
extern u32 native_fn_01ffb1d4(u32, u32);
extern u32 native_fn_01ffb340(void);
extern u32 native_fn_01ffb35c(void);
extern u32 native_fn_01ffb368(void);
extern u32 native_fn_02049604(u32, u32);
extern u32 native_fn_02049610(u32, u32);
extern u32 native_fn_0205e7a8(u32, u32);
extern u32 ov000_context_02246600_02223c54();
extern u8 native_data_021ceb54[];
extern u8 native_data_021ceb94[];
void native_itcm_01ff92cc(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    s8 temp_r0_2;
    u32 temp_r0;
    s32 var_r4;
    u32 temp_r5;

    var_r4 = 0;
    temp_r5 = ov000_context_02246600_02223c54();
    native_fn_01ffa440();
    if (M2C_FIELD(native_data_021ceb54, s32 *, 8) == 1) {
        if (M2C_FIELD(temp_r5, s8 *, 0x58) == 1) {
            if (native_fn_01ffb1d4(0xEU, 2U) == 1) {
                return;
            }
            goto block_8;
        }
        if (native_fn_01ffb1d4(3U, 4U) == 1) {
            return;
        }
        goto block_8;
    }
    if (native_fn_01ffb1d4(8U, 2U) == 1) {
        return;
    }
block_8:
    if (M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2) & 1) {
        if (native_fn_01ffb368() == 3) {
            var_r4 = 1;
        } else {
            temp_r0 = native_fn_01ffa44c(native_fn_01ffb368());
            if (temp_r0 != 0) {
                if ((M2C_FIELD(temp_r0, u16 *, 0x1C) == 0x10) && (M2C_FIELD((void *) ov000_context_02246600_02223c54(), s8 *, 0x59) == 1) && (M2C_FIELD(temp_r0, u16 *, 0x1E) == 1)) {
                    goto block_22;
                }
                if (M2C_FIELD(native_data_021ceb54, s32 *, 8) == 1) {
                    if (M2C_FIELD(temp_r5, s8 *, 0x58) == 0) {
                        native_fn_01ffae9c(0x10U, 6U, 0xCU, 0x52U);
                    } else {
                        native_fn_01ffae9c(0x10U, 0xFU, 4U, 0x52U);
                    }
                } else {
                    native_fn_01ffae9c(0x10U, 9U, 2U, 0x52U);
                }
                native_fn_01ffb060(1U);
                native_fn_01ffa484(native_fn_01ffb368());
                M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 0x19;
                native_fn_01ffa5ac((u32) native_data_021ceb94, 0x34U, 1U);
            } else {
block_22:
                native_fn_0205e7a8(-1U, 0x54U);
            }
        }
    } else if (M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2) & 2) {
        var_r4 = 1;
    }
    if (var_r4 == 1) {
        native_fn_0205e7a8(-1U, 0x53U);
        M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 4;
        if (M2C_FIELD(native_data_021ceb54, s32 *, 8) == 1) {
            temp_r0_2 = M2C_FIELD(temp_r5, s8 *, 0x58);
            if (temp_r0_2 == 1) {
                native_fn_01ffac9c(2U, 1U, 0xDU, 1U, 2U, 2U);
            } else {
                native_fn_01ffac9c(2U, 1U, 2U, 3U, 2U, (u32) (s16) (temp_r0_2 + 1));
            }
        } else {
            native_fn_01ffac9c(2U, 1U, 7U, 0U, 0U, 2U);
        }
        native_fn_01ffa804();
        return;
    }
    native_fn_02049604(native_fn_01ffb340(), 1U);
    native_fn_02049610(native_fn_01ffb340(), 0U);
}
