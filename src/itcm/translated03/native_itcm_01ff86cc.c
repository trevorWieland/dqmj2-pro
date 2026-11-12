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
extern u32 native_fn_01ffb12c();
extern u32 native_fn_01ffb340();
extern u32 native_fn_01ffb35c();
extern u32 native_fn_01ffb368();
extern u32 native_fn_01ffb6e0();
extern u32 native_fn_02049604();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_0205e814();
extern u32 native_fn_02061260();
extern u32 native_fn_020620e8();
extern u32 native_fn_02062378();
extern u32 native_fn_020642cc();
extern u32 native_fn_02088a2c();
extern u32 ov000_context_02246600_02223c54();
extern u8 native_data_021ceb54[];
u32 native_itcm_01ff86cc(void) {
    s32 var_r1;
    u16 temp_r0;
    u32 temp_r0_2;

    M2C_FIELD((void *) ov000_context_02246600_02223c54(), s8 *, 0x58) = 0;
    if (native_fn_02062378() != 0) {
        return native_fn_020620e8(0, 1);
    }
    temp_r0_2 = native_fn_01ffb12c(1, 0);
    if (temp_r0_2 == 1) {
        return temp_r0_2;
    }
    if (M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2) & 1) {
        if (native_fn_01ffb368() == 0) {
            var_r1 = 1;
        } else {
            var_r1 = 2;
        }
        M2C_FIELD(native_data_021ceb54, s32 *, 8) = var_r1;
        if (native_fn_01ffb368() == 1) {
            native_fn_02088a2c();
        }
        native_fn_0205e7a8(-1, 0x52);
        if (M2C_FIELD(native_data_021ceb54, s32 *, 8) == 1) {
            M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 2;
            native_fn_01ffac9c(2, 0, 2, 1, 2, 0);
        } else {
            M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 3;
            native_fn_01ffac9c(2, 0, 7, 0x11, 0, 2);
        }
        native_fn_02049604(native_fn_01ffb340(), 1);
        return native_fn_020620e8(0x1B, 1);
    }
    temp_r0 = M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 2);
    if (!(temp_r0 & 2)) {
        return (u32) temp_r0;
    }
    native_fn_020642cc(0);
    native_fn_0205e7a8(-1, 0x53);
    M2C_FIELD(native_data_021ceb54, s32 *, 8) = 4;
    M2C_FIELD(native_data_021ceb54, s32 *, 0xC) = 1;
    native_fn_0205e814(0, 0, 0xF);
    native_fn_01ffb6e0(1);
    return native_fn_02061260(1);
}
