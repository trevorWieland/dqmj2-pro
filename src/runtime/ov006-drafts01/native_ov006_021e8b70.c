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
extern u32 native_fn_0202a634();
extern u32 native_fn_02048a44();
extern u32 native_fn_0204b61c();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_ov006_021e648c();
extern u32 native_fn_ov006_021e7d98();
extern u32 native_fn_ov006_021e8044();
extern u32 native_fn_ov006_021e89f0();
extern u32 native_fn_ov006_021e8a28();
extern u32 native_fn_ov006_021e8a54();
extern u32 native_fn_ov006_021e8ae0();
extern u8 native_data_ov006_02218d90[];
extern u8 native_data_ov006_02218e18[];
extern u8 native_data_ov006_02218eb0[];
extern u8 native_data_ov006_02218f40[];
u32 native_ov006_021e8b70(u32 arg0, s32 arg1, s32 arg2) {
    u16 temp_r0_2;
    void *temp_r0;
    u16 temp_r1;
    u32 var_r4;

    var_r4 = native_fn_ov006_021e648c(arg2);
    if (arg2 != 0) {
        temp_r0 = (void *) native_fn_0202a634();
        temp_r1 = M2C_FIELD(temp_r0, u16 *, 2);
        if (temp_r1 & 1) {
            var_r4 = M2C_FIELD(((M2C_FIELD(native_data_ov006_02218d90, u32 *, 0x5C) * 0xC) + arg1), u32 *, 8);
            if (var_r4 != 0) {
                if (var_r4 != -1U) {
                    if (M2C_FIELD(native_data_ov006_02218d90, s32 *, 0x10) != 0) {
                        native_fn_0205e7a8(-1, 0x52);
                    }
                } else {
                    native_fn_0205e7a8(-1, 0x53);
                }
                native_fn_ov006_021e8044(3, M2C_FIELD(native_data_ov006_02218d90, u32 *, 0x5C));
            }
        } else if (temp_r1 & 2) {
            var_r4 = -1U;
            native_fn_0205e7a8(-1, 0x53);
            native_fn_ov006_021e8044(3, M2C_FIELD(native_data_ov006_02218d90, u32 *, 0x5C));
        } else if (temp_r1 & 0x800) {
            if (M2C_FIELD(native_data_ov006_02218d90, s32 (**)(u32, s32), 0x50)(M2C_FIELD(native_data_ov006_02218d90, u32 *, 0x5C), arg1) != 0) {
                native_fn_0205e7a8(-1, 0x57);
                native_fn_0204b61c(native_data_ov006_02218e18, 0);
                native_fn_ov006_021e7d98(1);
                native_fn_ov006_021e8044(1, M2C_FIELD(native_data_ov006_02218d90, u32 *, 0x5C));
            }
        } else {
            temp_r0_2 = M2C_FIELD(temp_r0, u16 *, 6);
            if (temp_r0_2 & 0x40) {
                M2C_FIELD(native_data_ov006_02218d90, u32 *, 0x5C) = native_fn_ov006_021e89f0(M2C_FIELD(native_data_ov006_02218d90, u32 *, 0x5C), arg0, arg1);
            } else if (temp_r0_2 & 0x80) {
                M2C_FIELD(native_data_ov006_02218d90, u32 *, 0x5C) = native_fn_ov006_021e8a28(M2C_FIELD(native_data_ov006_02218d90, u32 *, 0x5C), arg0, arg1);
            } else if (temp_r0_2 & 0x20) {
                M2C_FIELD(native_data_ov006_02218d90, u32 *, 0x5C) = native_fn_ov006_021e8a54(M2C_FIELD(native_data_ov006_02218d90, u32 *, 0x5C), arg0, arg1);
            } else if (temp_r0_2 & 0x10) {
                M2C_FIELD(native_data_ov006_02218d90, u32 *, 0x5C) = native_fn_ov006_021e8ae0(M2C_FIELD(native_data_ov006_02218d90, u32 *, 0x5C), arg0, arg1);
            } else {
                native_fn_0204b61c(native_data_ov006_02218e18, 1);
            }
        }
    }
    native_fn_02048a44(native_data_ov006_02218f40, 1);
    native_fn_02048a44(native_data_ov006_02218eb0, 1);
    return var_r4;
}
