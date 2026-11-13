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
extern u32 native_fn_01ffac9c(u32, u32, u32, u32, u32, u32);
extern u32 native_fn_01ffafb8(void);
extern u32 native_fn_01ffb35c(void);
extern u32 native_fn_0205e7a8(u32, u32);
extern u32 ov000_context_02246600_02223c54();
extern u8 native_data_021ceb54[];
void native_itcm_01ff96bc(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    s8 temp_r0;
    s8 temp_r4;
    u32 temp_r5;

    temp_r4 = M2C_FIELD((void *) ov000_context_02246600_02223c54(), s8 *, 0x5A);
    temp_r5 = ov000_context_02246600_02223c54();
    if (!(M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2) & 0xFF7)) {
        return;
    }
    native_fn_0205e7a8(-1U, 0x52U);
    native_fn_01ffafb8();
    M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 4;
    if (M2C_FIELD(native_data_021ceb54, s32 *, 8) == 1) {
        temp_r0 = M2C_FIELD(temp_r5, s8 *, 0x58);
        if (temp_r0 == 1) {
            native_fn_01ffac9c(2U, (u32) temp_r4, 0xDU, 1U, 2U, 2U);
            return;
        }
        native_fn_01ffac9c(2U, (u32) temp_r4, 2U, 3U, 2U, (u32) (s16) (temp_r0 + 1));
        return;
    }
    native_fn_01ffac9c(2U, (u32) temp_r4, 7U, 0U, 0U, 2U);
}
