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
extern u32 native_fn_0205e7a8();
extern u32 native_fn_ov000_021eb8d8();
extern u8 native_data_ov000_0222b8b8[];
typedef struct {
    u8 unknown_0[0x10];
    s32 field_10;
    u8 unknown_14[0xc];
    s8 field_20;
    u8 unknown_21[0xdf];
    s8 field_100;
} Record_native_data_ov000_02236980;
extern Record_native_data_ov000_02236980 native_data_ov000_02236980;
u32 native_ov000_021eb778(s32 *arg0) {
    s8 var_r4;
    u32 temp_r0;

    var_r4 = native_data_ov000_02236980.field_20;
    temp_r0 = native_fn_0202a634();
    switch (native_data_ov000_02236980.field_20) {
    case 0:
        if (M2C_FIELD(temp_r0, u16 *, 2) & 1) {
            switch (native_data_ov000_02236980.field_10) {
            case 0:
                native_fn_0205e7a8(-1, 0x52);
                var_r4 = 1;
                break;
            case 1:
                native_fn_0205e7a8(-1, 0x52);
                var_r4 = 2;
                break;
            case 2:
                native_fn_0205e7a8(-1, 0x53);
                native_data_ov000_02236980.field_100 = 6;
                break;
            }
        }
        break;
    case 1:
        if (M2C_FIELD(temp_r0, u16 *, 2) & 1) {
            if (native_fn_ov000_021eb8d8(*(u32 *)(native_data_ov000_0222b8b8 + (native_data_ov000_02236980.field_10 * 4)), 1) != 0) {
                native_fn_0205e7a8(-1, 0x52);
            } else {
                native_fn_0205e7a8(-1, 0x54);
            }
            *arg0 = 1;
        }
        break;
    case 2:
        if (M2C_FIELD(temp_r0, u16 *, 2) & 1) {
            if (native_fn_ov000_021eb8d8(*(u32 *)(native_data_ov000_0222b8b8 + (native_data_ov000_02236980.field_10 * 4)), 0) != 0) {
                native_fn_0205e7a8(-1, 0x52);
            } else {
                native_fn_0205e7a8(-1, 0x54);
            }
            *arg0 = 1;
        }
        break;
    }
    return (u32) var_r4;
}
