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
extern u8 *native_fn_01ffa724();
extern u32 native_fn_01ffa824();
extern u32 native_fn_01ffa84c();
extern u32 native_fn_02044414();
extern u32 native_fn_02044564();
extern u32 ov001_side_slot_record_021db438();
extern u32 ov001_mode_byte_021db530();
extern u32 native_fn_ov001_021e824c();
extern u32 native_fn_ov001_02203308();
extern u32 native_fn_ov001_02203320();
__declspec(align(4)) extern u8 native_data_ov001_02239d04[];
u32 native_ov001_022030b8(void) {
    u8 *sp8;
    u32 sp4;
    s32 var_r2;
    s32 var_r4;
    u32 temp_r7;
    s32 var_r8;
    u32 temp_r0;
    u32 temp_r0_2;
    u8 *temp_r0_3;
    u8 *temp_r9;
    u8 temp_r11;
    u8 temp_r2;
    void *temp_r0_4;
    void *temp_r1;
    void *temp_r3;
    void *var_r10;

    temp_r7 = ov001_mode_byte_021db530(1);
    temp_r11 = (u8) native_fn_01ffa824();
    temp_r0 = native_fn_01ffa84c();
    sp4 = temp_r0;
    temp_r0_2 = native_fn_02044414();
    temp_r0_3 = native_fn_01ffa724(temp_r11, temp_r0_2 + 0x8000);
    sp8 = temp_r0_3;
    temp_r9 = native_fn_01ffa724(temp_r0, temp_r0_2 + 0x8000);
    if (temp_r0_3 == 0) {
        return 0U;
    }
    if (temp_r9 == 0) {
        return 0U;
    }
    native_fn_ov001_02203308(1, M2C_FIELD(temp_r9, u8 *, 0));
    if (native_fn_ov001_02203320(1) != 1) {
        var_r8 = 0;
        if ((s32) temp_r7 > 0) {
            var_r10 = temp_r9 + 4;
            do {
                temp_r0_4 = (void *) ov001_side_slot_record_021db438(1, var_r8);
                temp_r2 = M2C_FIELD((temp_r9 + var_r8), u8 *, 1);
                if (M2C_FIELD(temp_r0_4, u8 *, 0x1FE) != temp_r2) {
                    M2C_FIELD(temp_r0_4, u8 *, 0x1FE) = temp_r2;
                    M2C_FIELD(temp_r0_4, u8 *, 0x35D) = (u8) (M2C_FIELD(temp_r0_4, u8 *, 0x35D) | 4);
                }
                if (M2C_FIELD(var_r10, u8 *, 2) == 1) {
                    var_r2 = 0;
                } else {
                    var_r2 = 1;
                }
                native_fn_ov001_021e824c(var_r8, M2C_FIELD(var_r10, u16 *, 0), var_r2, M2C_FIELD(var_r10, s8 *, 3), M2C_FIELD(var_r10, u8 *, 4));
                var_r8 += 1;
                var_r10 += 6;
            } while (var_r8 < (s32) temp_r7);
        }
    }
    if ((s32) temp_r11 < (s32) sp4) {
        native_fn_02044564(M2C_FIELD(sp8, s32 *, 0x18));
    } else {
        native_fn_02044564(M2C_FIELD(temp_r9, s32 *, 0x18));
    }
    var_r4 = 0;
    do {
        temp_r3 = temp_r9 + (var_r4 * 4);
        M2C_FIELD(native_data_ov001_02239d04 + var_r4 * 4, s32 *, 0x50) = (s32) M2C_FIELD(temp_r3, s32 *, 0x1C);
        M2C_FIELD(native_data_ov001_02239d04 + var_r4 * 4, s32 *, 0x5C) = (s32) M2C_FIELD(temp_r3, s32 *, 0x28);
        var_r4 += 1;
    } while (var_r4 < 3);
    return 1U;
}
