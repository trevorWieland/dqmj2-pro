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
extern u32 native_fn_020273d8();
extern u32 native_fn_020273f0();
extern u32 native_fn_020404f0();
extern u32 native_fn_020406a8();
extern u32 native_fn_020406c8();
extern u32 native_fn_02040820();
extern u32 native_fn_02041898();
extern u32 native_fn_02045654();
extern u32 native_fn_020612ec();
extern u32 native_fn_0206157c();
extern u32 native_fn_02061950();
extern u32 native_fn_02062a50();
extern u32 native_fn_0206539c();
extern u32 native_fn_02067340();
extern u32 native_fn_02067380();
extern u32 native_fn_0206dcd0();
extern u32 native_fn_0206de8c();
extern u8 native_data_020f6054[];
u32 native_main_0203d96c(void) {
    s32 var_r2;
    s32 var_r5;
    u32 temp_r0;
    u32 temp_r5;
    u32 var_r4;

    var_r4 = 0;
    if (M2C_FIELD(native_data_020f6054, u8 *, 0x27) == 0) {
        temp_r0 = native_fn_0206539c();
        var_r5 = -1;
        var_r2 = 0;
loop_2:
        if (temp_r0 & (1 << var_r2)) {
            var_r5 = var_r2;
        } else {
            var_r2 += 1;
            if (var_r2 < 3) {
                goto loop_2;
            }
        }
        if (var_r5 < 0) {
            M2C_FIELD(native_data_020f6054, u8 *, 0x27) = 0x64U;
        } else {
            native_fn_020406a8(1);
            native_fn_02067340(2);
            native_fn_020612ec(1, 0, 0x6000, 1);
            native_fn_02062a50(var_r5);
            native_fn_0206dcd0();
            native_fn_0206de8c();
            native_fn_02061950(1);
            native_fn_02045654(1);
            native_fn_02045654(2);
            native_fn_02045654(3);
            native_fn_020406c8(6);
            M2C_FIELD(native_data_020f6054, u32 *, 0x38) = native_fn_020273d8(1U);
            M2C_FIELD(native_data_020f6054, u8 *, 0x27) = 0xAU;
        }
    }
    if (M2C_FIELD(native_data_020f6054, u8 *, 0x27) == 0xA) {
        M2C_FIELD(native_data_020f6054, u8 *, 0x27) = 0x14U;
    }
    if (M2C_FIELD(native_data_020f6054, u8 *, 0x27) == 0x14) {
        temp_r5 = native_fn_02067380();
        if ((native_fn_0206157c() != 0) && (temp_r5 != 0)) {
            M2C_FIELD(native_data_020f6054, u8 *, 0x27) = 0x1EU;
        }
    }
    if ((M2C_FIELD(native_data_020f6054, u8 *, 0x27) == 0x1E) && ((native_fn_020273f0() == 0) || (native_fn_020273f0() == 0xC))) {
        M2C_FIELD(native_data_020f6054, u8 *, 0x27) = 0x32U;
    }
    if (M2C_FIELD(native_data_020f6054, u8 *, 0x27) == 0x32) {
        native_fn_02041898(2);
        native_fn_020273d8(M2C_FIELD(native_data_020f6054, u32 *, 0x38));
        M2C_FIELD(native_data_020f6054, u8 *, 0x27) = 0x3CU;
    }
    if (M2C_FIELD(native_data_020f6054, u8 *, 0x27) == 0x3C) {
        M2C_FIELD(native_data_020f6054, u8 *, 0x27) = 0x64U;
    }
    if (M2C_FIELD(native_data_020f6054, u8 *, 0x27) == 0x64) {
        native_fn_020404f0(1);
        M2C_FIELD(native_data_020f6054, u8 *, 0x27) = 0U;
        var_r4 = 1;
    }
    native_fn_02040820();
    return var_r4;
}
