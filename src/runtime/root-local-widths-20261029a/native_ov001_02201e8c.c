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
extern u32 native_fn_02008d78();
extern u32 native_fn_02041814();
extern u32 native_fn_0206cc3c();
extern u32 native_fn_0206d7f8();
extern u32 native_fn_ov001_021db508();
extern u32 native_fn_ov001_021fcf58();
extern u32 native_fn_ov001_021fe9b0();
extern u32 ov001_table_f0_entry_02202360();
extern u32 native_fn_ov001_022034ac();
extern u32 native_fn_ov001_022042c4();
extern u32 native_fn_ov001_02204d00();
extern u32 native_fn_ov001_0220b3e4();
typedef struct {
    u8 unknown_0[0x1];
    s8 field_1;
} Record_native_data_ov001_0222ed34;
extern Record_native_data_ov001_0222ed34 native_data_ov001_0222ed34;
extern u8 native_data_ov001_0222edc8[];
typedef struct {
    u8 unknown_0[0xa];
    s8 field_a;
    u8 unknown_b[0x1];
    s8 field_c;
} Record_native_data_ov001_02239c10;
extern Record_native_data_ov001_02239c10 native_data_ov001_02239c10;
extern u8 native_data_ov001_0223a030[];
u32 native_ov001_02201e8c(void) {
    u32 temp_r0;
    void *temp_r2;
    u8 *temp_r4;
    u32 temp_r5;
    u32 temp_r5_2;
    u8 var_r5;
    u32 temp_r6;
    u32 temp_r6_2;
    u8 var_r7;

    temp_r4 = ov001_table_f0_entry_02202360(native_data_ov001_02239c10.field_c);
    if (native_fn_02041814() == 1) {
        return 0U;
    }
    temp_r6 = native_fn_ov001_021db508(0, 0U);
    temp_r5 = native_fn_ov001_021db508(0, 1U);
    native_fn_ov001_0220b3e4(0, temp_r6, temp_r5, native_fn_ov001_021db508(0, 2U));
    temp_r6_2 = native_fn_ov001_021db508(2, 0U);
    temp_r5_2 = native_fn_ov001_021db508(2, 1U);
    native_fn_ov001_0220b3e4(2, temp_r6_2, temp_r5_2, native_fn_ov001_021db508(2, 2U));
    var_r7 = 0;
    do {
        temp_r0 = native_fn_ov001_021db508(0, var_r7);
        temp_r2 = native_data_ov001_0223a030 + (var_r7 * 4);
        var_r7 += 1;
        M2C_FIELD(temp_r2, u32 *, 0x208) = temp_r0;
    } while ((u32) var_r7 < 3U);
    native_fn_ov001_022042c4(temp_r4 + 0x18);
    native_data_ov001_0222ed34.field_1 = (s8) *(u32 *)temp_r4;
    native_fn_0206d7f8();
    native_fn_0206cc3c(2);
    native_fn_ov001_021fe9b0();
    native_fn_ov001_021fcf58();
    var_r5 = 0;
    do {
        if ((s8) native_data_ov001_0222edc8[var_r5] != 0x7F) {
            native_fn_ov001_02204d00();
        }
        var_r5 += 1;
    } while ((u32) var_r5 < 3U);
    native_fn_02008d78(0x07000400, 0, 0x400);
    native_fn_ov001_022034ac();
    native_data_ov001_02239c10.field_a = 0x16;
    return 0U;
}
