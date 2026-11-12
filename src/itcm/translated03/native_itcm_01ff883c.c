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
extern u32 native_fn_01ffa8b8();
extern u32 native_fn_01ffac9c();
extern u32 native_fn_01ffb12c();
extern u32 native_fn_01ffb35c();
extern u32 native_fn_01ffb368();
extern u32 native_fn_0203d294();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_020620e8();
extern u32 native_fn_ov000_021f6cd0();
extern u32 ov000_context_02246600_02223c54();
extern u8 native_data_021ceb54[];
u32 native_itcm_01ff883c(void) {
    u16 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;
    u32 temp_r4;

    temp_r4 = ov000_context_02246600_02223c54();
    M2C_FIELD(native_data_021ceb54, u32 *, 0x58) = native_fn_0203d294(0x7FFFFFFF);
    native_fn_01ffa8b8();
    temp_r0_3 = native_fn_01ffb12c(3, 0);
    if (temp_r0_3 == 1) {
        return temp_r0_3;
    }
    temp_r0_2 = native_fn_ov000_021f6cd0();
    if (temp_r0_2 == 1) {
        return temp_r0_2;
    }
    if (M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2) & 1) {
        M2C_FIELD(temp_r4, s8 *, 0x58) = (s8) native_fn_01ffb368();
        native_fn_0205e7a8(-1, 0x52);
        M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 4;
        if (M2C_FIELD(temp_r4, s8 *, 0x58) == 0) {
            return native_fn_01ffac9c(2, 0, 2, 3, 2, 1);
        }
        return native_fn_01ffac9c(2, 0, 0xD, 1, 2, 2);
    }
    temp_r0 = M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2);
    if (!(temp_r0 & 2)) {
        return (u32) temp_r0;
    }
    native_fn_0205e7a8(-1, 0x53);
    M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 0;
    native_fn_01ffac9c(2, 0, 0, 1, 0, 0);
    return native_fn_020620e8(0, 1);
}
