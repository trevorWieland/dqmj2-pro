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
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_02027400();
extern u32 native_fn_020bae44();
extern u32 ov006_noop_021e3cd4();
extern u32 native_fn_ov006_021e3f28();
extern u32 native_fn_ov006_021e4b24();
extern u32 native_fn_ov006_021e4d1c();
extern u32 native_fn_ov006_021e4e04();
extern u32 native_fn_ov006_021e7d98();
extern u32 native_fn_ov006_021e7fe0();
extern u32 native_fn_ov006_021e802c();
extern u32 ov006_commit_mode_transition_021e9148();
extern u8 native_data_ov006_02207d50[];
extern u8 native_data_ov006_02218d30[];
extern u8 native_data_ov006_02218d54[];
u32 native_ov006_021e4ec4(void) {
    u32 temp_r0;

    ov006_noop_021e3cd4();
    native_fn_020bae44();
    native_fn_ov006_021e4b24();
    if (M2C_FIELD(native_data_ov006_02218d30, s32 (**)(u8 *, u32 (*)(), u32 (*)()), 0xC)(native_data_ov006_02218d54, native_fn_ov006_021e4d1c, native_fn_ov006_021e4e04) != 0) {
        native_fn_ov006_021e7fe0();
        native_fn_ov006_021e7d98(0);
        ov006_commit_mode_transition_021e9148(native_data_ov006_02207d50, 0);
        M2C_FIELD(native_data_ov006_02218d30, s32 *, 0) = 0;
        temp_r0 = native_fn_02027400();
        if (temp_r0 != 0xF) {
            return temp_r0;
        }
        M2C_FIELD(native_data_ov006_02218d30, s32 *, 0) = 5;
        return (u32) native_data_ov006_02218d30;
    }
    native_fn_ov006_021e802c(M2C_FIELD(native_data_ov006_02218d30, s32 *, 0x18));
    return native_fn_ov006_021e3f28(M2C_FIELD(native_data_ov006_02218d30, s32 *, 0x14));
}
