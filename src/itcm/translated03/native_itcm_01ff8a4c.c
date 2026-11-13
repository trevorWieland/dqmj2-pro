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
extern u32 native_fn_01ffac9c();
extern u32 native_fn_01ffae5c();
extern u32 native_fn_01ffb12c();
extern u32 native_fn_01ffb35c();
extern u32 native_fn_01ffb368();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_ov000_021f6cd0();
extern u32 ov000_context_02246600_02223c54();
extern u8 native_data_021ceb54[];
u32 native_itcm_01ff8a4c(void) {
    u16 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;
    u32 temp_r0_4;
    u32 temp_r0_5;
    u32 temp_r4;
    u32 temp_r4_2;

    temp_r4 = ov000_context_02246600_02223c54();
    if (M2C_FIELD(native_data_021ceb54, s32 *, 8) == 1) {
        if (M2C_FIELD(temp_r4, s8 *, 0x58) == 0) {
            temp_r0_5 = native_fn_01ffb12c(3, 2);
            if (temp_r0_5 == 1) {
                return temp_r0_5;
            }
            goto block_8;
        }
        temp_r0_4 = native_fn_01ffb12c(0xE, 0);
        if (temp_r0_4 == 1) {
            return temp_r0_4;
        }
        goto block_8;
    }
    temp_r0_3 = native_fn_01ffb12c(8, 0);
    if (temp_r0_3 == 1) {
        return temp_r0_3;
    }
block_8:
    if (M2C_FIELD(native_data_021ceb54, s32 *, 8) != 1) {
        temp_r0_2 = native_fn_ov000_021f6cd0();
        if (temp_r0_2 == 1) {
            return temp_r0_2;
        }
    }
    if (M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2) & 1) {
        temp_r4_2 = ov000_context_02246600_02223c54();
        M2C_FIELD(temp_r4_2, s8 *, 0x5A) = (s8) native_fn_01ffb368();
        M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 5;
        return native_fn_01ffae5c(0x10, 6, 0, 0x52, 0);
    }
    temp_r0 = M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2);
    if (!(temp_r0 & 2)) {
        return (u32) temp_r0;
    }
    native_fn_0205e7a8(-1, 0x53);
    if (M2C_FIELD(native_data_021ceb54, s32 *, 8) == 1) {
        M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 2;
        return native_fn_01ffac9c(2, M2C_FIELD(temp_r4, s8 *, 0x58), 2, 1, 2, 0);
    }
    M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 3;
    return native_fn_01ffac9c(2, M2C_FIELD(temp_r4, s8 *, 0x59), 7, 0x11, 0, 2);
}
