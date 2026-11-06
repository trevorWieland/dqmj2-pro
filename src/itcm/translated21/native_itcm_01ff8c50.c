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
extern u32 native_fn_01ff8bc4(void);
extern u32 native_fn_01ffa01c(u32);
extern u32 native_fn_01ffa2a4(u32);
extern u32 native_fn_01ffa3dc(u32);
extern u32 native_fn_01ffac9c(u32, u32, u32, u32, u32, u32);
extern u32 native_fn_01ffae5c(u32, u32, u32, u32, u32);
extern u32 native_fn_01ffae9c(u32, u32, u32, u32);
extern u32 native_fn_01ffafb8(void);
extern u32 native_fn_01ffb060(u32);
extern u32 native_fn_01ffb35c(void);
extern u32 native_fn_01ffb378(void);
extern u32 native_fn_0205e7a8(u32, u32);
extern u32 native_fn_02061260(u32);
extern u32 native_fn_02084400(u32, u32);
extern u32 native_fn_020894e0(void);
extern u32 native_fn_ov000_02223c54();
extern u8 native_data_021ceb54[];
void native_itcm_01ff8c50(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    s8 temp_r4;
    u32 temp_r5;

    temp_r4 = M2C_FIELD((void *) native_fn_ov000_02223c54(), s8 *, 0x5A);
    temp_r5 = native_fn_ov000_02223c54();
    if ((M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2) != 1) && !(M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2) & 2)) {
        return;
    }
    native_fn_01ffafb8();
    if ((native_fn_01ffb378() == 0) && !(M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2) & 2)) {
        native_fn_0205e7a8(-1U, 0x52U);
        M2C_FIELD(native_data_021ceb54, s32 *, 0x54) = 0;
        if (M2C_FIELD(native_data_021ceb54, s32 *, 8) == 1) {
            native_fn_01ffa01c(0U);
            if (temp_r4 == 0) {
                M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 0xF;
                if (M2C_FIELD(temp_r5, s8 *, 0x58) == 0) {
                    native_fn_01ffa01c(1U);
                    native_fn_01ffae9c(0x10U, 6U, 0xFU, -1U);
                    native_fn_01ffb060(1U);
                    native_fn_01ffa2a4(1U);
                    return;
                }
                native_fn_01ffae5c(0x10U, 0xFU, 1U, -1U, 1U);
                native_fn_01ffa2a4(2U);
                native_fn_02061260(1U);
                return;
            }
            M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 0x18;
            native_fn_01ffac9c(3U, 0U, 2U, 5U, 2U, (u32) (s16) (M2C_FIELD(temp_r5, s8 *, 0x58) + 1));
            if (M2C_FIELD(temp_r5, s8 *, 0x58) == 0) {
                native_fn_01ffa01c(1U);
                native_fn_01ffa3dc(1U);
                return;
            }
            native_fn_01ffa3dc(2U);
            return;
        }
        native_fn_01ffa01c(1U);
        if (temp_r4 == 0) {
            M2C_FIELD(temp_r5, s8 *, 0x58) = 0;
            M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 0xF;
            native_fn_01ffae9c(0x10U, 9U, 0U, -1U);
            native_fn_01ffb060(1U);
            native_fn_01ffa2a4(0x10U);
            return;
        }
        M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 0x18;
        native_fn_01ffac9c(3U, 0U, 2U, 5U, 0U, 2U);
        native_fn_02084400((u32) native_fn_01ff8bc4, 0U);
        native_fn_01ffa3dc(0x10U);
        return;
    }
    native_fn_020894e0();
    M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 4;
    if (M2C_FIELD(native_data_021ceb54, s32 *, 8) == 1) {
        if (M2C_FIELD(temp_r5, s8 *, 0x58) == 0) {
            native_fn_01ffac9c(2U, (u32) temp_r4, 2U, 3U, 2U, 1U);
            return;
        }
        native_fn_01ffac9c(2U, (u32) temp_r4, 0xDU, 1U, 2U, 2U);
        return;
    }
    native_fn_01ffac9c(2U, (u32) temp_r4, 7U, 0U, 0U, 2U);
}
