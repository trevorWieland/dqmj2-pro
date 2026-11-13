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
extern u32 native_fn_020443ec();
extern u32 native_fn_0204458c();
extern u32 ov001_mode_byte_021db530();
extern u32 native_fn_ov001_021e13a8();
extern u32 native_fn_ov001_021e81f0();
extern u32 native_fn_ov001_021f949c();
extern u32 native_fn_ov001_021fbe88();
extern u32 native_fn_ov001_021fe2b8();
extern u32 native_fn_ov001_02201504();
extern u32 native_fn_ov001_022021fc();
extern u32 native_fn_ov001_02202218();
extern u32 native_fn_ov001_0220225c();
extern u32 ov001_table_f0_entry_02202360();
extern u32 native_fn_ov001_02202f98();
extern u32 native_fn_ov001_02202fb4();
extern u32 native_fn_ov001_02202fe4();
extern u32 native_fn_ov001_02204590();
extern u32 native_fn_ov001_0220b70c();
typedef struct {
    u8 unknown_0[0x2];
    s8 field_2;
} Record_native_data_ov001_0222ed34;
extern Record_native_data_ov001_0222ed34 native_data_ov001_0222ed34;
extern u8 native_data_ov001_0222edc8[];
typedef struct {
    u8 unknown_0[0xa];
    u8 field_a;
    u8 unknown_b[0x1];
    s8 field_c;
    u8 unknown_d[0x3f];
    s32 field_4c;
} Record_native_data_ov001_02239c10;
extern Record_native_data_ov001_02239c10 native_data_ov001_02239c10;
extern u8 native_data_ov001_02239d6c[];
u32 native_ov001_0220054c(u32 arg0) {
    s32 temp_r0;
    u32 var_r4;
    u8 *temp_r5;
    s32 var_r6;
    u8 *temp_r6;
    u8 *var_r7;
    u8 *var_r8;

    var_r4 = 0;
    temp_r5 = ov001_table_f0_entry_02202360(native_data_ov001_02239c10.field_c);
    switch (arg0) {
    default:
        break;
    case 0:
        temp_r0 = (s32) ov001_mode_byte_021db530(0);
        var_r6 = 0;
        if (temp_r0 > 0) {
            var_r7 = native_data_ov001_0222edc8;
            var_r8 = native_data_ov001_02239d6c;
            do {
                if ((s8) *var_r7 != 0x7F) {
                    native_fn_ov001_021e81f0(var_r6, M2C_FIELD(var_r8, s32 *, 4), M2C_FIELD(var_r8, s32 *, 8), M2C_FIELD(var_r8, s32 *, 0xC));
                }
                var_r6 += 1;
                var_r7 += 1;
                var_r8 += 0xC;
            } while (var_r6 < temp_r0);
        }
        native_fn_ov001_02202218(8);
        if ((native_fn_020443ec() != 2) || (native_fn_0204458c() != 1)) {
            native_fn_ov001_021e13a8(2);
        } else {
            native_fn_ov001_0220225c();
        }
        var_r4 = 1;
        native_fn_ov001_021f949c(0x52, 1);
        break;
    case 1:
        if (native_fn_ov001_02202f98() != 0) {
            native_fn_ov001_02202218(1);
            native_data_ov001_02239c10.field_a = 6U;
            native_fn_ov001_021f949c(0x52, 1);
        } else {
            native_fn_ov001_021f949c(0x54, 1);
        }
        break;
    case 3:
        if (native_data_ov001_02239c10.field_4c == 0) {
            native_fn_ov001_02202218(3);
            native_data_ov001_02239c10.field_a = 6U;
            native_fn_ov001_021f949c(0x52, 1);
            var_r4 = 1;
        } else {
            if (native_fn_ov001_021fbe88() == 3) {
                native_data_ov001_0222ed34.field_2 = 0;
                native_fn_ov001_02201504();
                native_data_ov001_02239c10.field_a = 8U;
            }
            native_fn_ov001_021f949c(0x54, 1);
        }
        break;
    case 4:
        if (native_fn_ov001_02202fb4() != 0) {
            temp_r6 = ov001_table_f0_entry_02202360(4);
            native_fn_ov001_02202218(4);
            native_fn_ov001_0220b70c(1);
            native_fn_ov001_021fe2b8(0, 1);
            native_data_ov001_02239c10.field_a = 4U;
            *(u32 *)temp_r6 = 0;
            native_fn_ov001_021f949c(0x52, 1);
        } else {
            native_fn_ov001_021f949c(0x54, 1);
        }
        break;
    case 2:
        native_fn_ov001_02202218(2);
        native_data_ov001_02239c10.field_a = 6U;
        native_fn_ov001_021f949c(0x52, 1);
        break;
    case 5:
        if (native_fn_ov001_02202fe4() != 0) {
            if (native_fn_ov001_022021fc() != 0) {
                native_fn_ov001_021e13a8(4);
                var_r4 = 1;
            } else {
                native_data_ov001_02239c10.field_a = 4U;
                native_fn_ov001_021fe2b8(0, 1);
                native_fn_ov001_02202218(5);
            }
            native_fn_ov001_021f949c(0x52, 1);
        } else {
            native_fn_ov001_021f949c(0x54, 1);
        }
        break;
    }
    if (native_data_ov001_02239c10.field_a != 3) {
        native_fn_ov001_02204590(temp_r5 + 0x18, 0x7D);
    }
    return var_r4;
}
