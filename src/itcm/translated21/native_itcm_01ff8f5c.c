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
extern u32 native_fn_01ff8eec(void);
extern u32 native_fn_01ffa33c(void);
extern u32 native_fn_01ffa348(u32);
extern u32 native_fn_01ffa358(void);
extern u32 native_fn_01ffa5ac(u32, u32, u32);
extern u32 native_fn_01ffa5fc(u32, u32);
extern u32 native_fn_01ffa804(void);
extern u32 native_fn_01ffa84c(void);
extern u32 native_fn_01ffa878(void);
extern u32 native_fn_01ffae5c(u32, u32, u32, u32, u32);
extern u32 native_fn_01ffae9c(u32, u32, u32, u32);
extern u32 native_fn_01ffafb8(void);
extern u32 native_fn_01ffb03c(void);
extern u32 native_fn_01ffb060(u32);
extern u32 native_fn_01ffb35c(void);
extern u32 native_fn_01ffb378(void);
extern u32 native_fn_02048034(u32, u32);
extern u32 native_fn_020620e8(u32, u32);
extern u32 native_fn_0208420c(void);
extern u32 native_fn_020889cc(u32);
extern u32 native_fn_020894e0(void);
extern u32 ov000_context_02246600_02223c54();
extern u8 native_data_021ceb54[];
extern u8 native_data_021ceb94[];
void native_itcm_01ff8f5c(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    u32 temp_r0;
    u32 temp_r4;

    temp_r4 = ov000_context_02246600_02223c54();
    native_fn_020889cc(1U);
    if (M2C_FIELD(temp_r4, s8 *, 0x58) == 1) {
        native_fn_01ff8eec();
        if (((M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2) & 1) || (M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2) & 2)) && (M2C_FIELD(native_data_021ceb54, s32 *, 0xC) != 0x17)) {
            native_fn_020894e0();
            native_fn_01ffafb8();
            if ((native_fn_01ffb378() == 0) && (M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2) & 1)) {
                if (native_fn_01ffa358() < 2U) {
                    M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 0x17;
                    native_fn_01ffae9c(0x10U, 0xFU, 3U, -1U);
                    return;
                }
                native_fn_0208420c();
                M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 0x13;
                M2C_FIELD(native_data_021ceb54, s16 *, 0) = 0x5A;
                native_fn_01ffae9c(0x10U, 0xFU, 0x1BU, -1U);
                native_fn_01ffb060(1U);
                return;
            }
            M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 0x11;
            native_fn_01ffa348(0U);
            native_fn_020620e8(0x1BU, 1U);
            if (native_fn_01ffa358() > 1U) {
                M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 0x15;
                native_fn_01ffae9c(0x10U, 0xFU, 5U, -1U);
                M2C_FIELD(native_data_021ceb54, s32 *, 0x54) = 2;
                native_fn_01ffa5ac((u32) native_data_021ceb94, 0x34U, 2U);
                return;
            }
            native_fn_01ffae9c(0x10U, 6U, 0x16U, -1U);
            native_fn_01ffb060(1U);
            native_fn_01ffa804();
            M2C_FIELD(native_data_021ceb54, s16 *, 0) = 0;
            return;
        }
        native_fn_01ffb03c();
        goto block_13;
    }
block_13:
    native_fn_01ffa5ac((u32) native_data_021ceb94, 0x34U, 1U);
    if (M2C_FIELD(temp_r4, s8 *, 0x58) == 1) {
        return;
    }
    if ((M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2) & 2) && (M2C_FIELD(native_data_021ceb54, s32 *, 0xC) != 0x17)) {
        native_fn_01ffafb8();
        M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 0x11;
        native_fn_01ffa804();
        native_fn_01ffae9c(0x10U, 6U, 0x16U, 0x53U);
        native_fn_01ffb060(1U);
        M2C_FIELD(native_data_021ceb54, s16 *, 0) = 0;
        return;
    }
    if (native_fn_01ffa33c() == 1) {
        return;
    }
    native_fn_01ffa878();
    temp_r0 = native_fn_01ffa5fc(native_fn_01ffa84c(), 1U);
    if (temp_r0 == 0) {
        return;
    }
    native_fn_0208420c();
    native_fn_01ffafb8();
    native_fn_02048034(temp_r0, 0U);
    if (M2C_FIELD(native_data_021ceb54, s32 *, 8) == 1) {
        native_fn_01ffae5c(0x10U, 6U, 0xBU, 0x57U, 0U);
    } else {
        native_fn_01ffae5c(0x10U, 9U, 1U, 0x57U, 0U);
    }
    M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 0x12;
}
