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
extern u32 native_fn_02048fcc();
extern u32 native_fn_02049748();
extern u32 native_fn_ov001_021fe2b8();
extern u32 native_fn_ov001_021feeb4();
extern u32 native_fn_ov001_02202218();
extern u32 native_fn_ov001_02202360();
extern u32 native_fn_ov001_022023c4();
extern u32 native_fn_ov001_02202b84();
extern u32 native_fn_ov001_022042c4();
extern u32 native_fn_ov001_02204590();
typedef struct {
    u8 unknown_0[0xa];
    u8 field_a;
    u8 unknown_b[0x1];
    s8 field_c;
} Record_native_data_ov001_02239c10;
extern Record_native_data_ov001_02239c10 native_data_ov001_02239c10;
u32 native_ov001_022011c0(void) {
    s8 temp_r5;
    u32 temp_r0;

    temp_r0 = native_fn_ov001_02202360(native_data_ov001_02239c10.field_c);
    native_fn_ov001_022042c4(temp_r0 + 0xA8);
    switch (native_data_ov001_02239c10.field_c) {
    default:
        break;
    case 1:
        if (M2C_FIELD(temp_r0, u8 *, 0x13) == 3) {
            native_fn_ov001_021fe2b8(0, 1);
            native_fn_ov001_02202b84();
            native_data_ov001_02239c10.field_a = 4U;
            if (M2C_FIELD(temp_r0, u8 *, 0x14) == 1) {
                M2C_FIELD(temp_r0, s8 *, 0xA) = -1;
            }
        } else {
            temp_r5 = M2C_FIELD(temp_r0, s8 *, 0x12);
            native_fn_02048fcc(temp_r0);
            native_fn_ov001_022023c4(0x85);
            native_fn_ov001_02202218(0);
            native_fn_ov001_021fe2b8(2, 1);
            native_data_ov001_02239c10.field_a = 3U;
            M2C_FIELD(temp_r0, s8 *, 0x12) = temp_r5;
            M2C_FIELD(temp_r0, s8 *, 8) = -1;
            M2C_FIELD(temp_r0, u8 *, 0x13) = 0U;
        }
        break;
    case 3:
        native_fn_02049748(temp_r0);
        native_fn_ov001_022023c4(0x85);
        native_fn_ov001_02202218(0);
        native_fn_ov001_021fe2b8(2, 1);
        native_data_ov001_02239c10.field_a = 3U;
        break;
    case 4:
        native_fn_02049748(temp_r0);
        native_fn_ov001_022023c4(0x85);
        native_fn_ov001_021fe2b8(0, 1);
        native_data_ov001_02239c10.field_a = 4U;
        break;
    case 2:
        native_fn_02049748(temp_r0);
        native_fn_ov001_022023c4(0x85);
        native_fn_ov001_021fe2b8(2, 1);
        native_fn_ov001_02202218(0);
        native_data_ov001_02239c10.field_a = 3U;
        break;
    }
    if (native_data_ov001_02239c10.field_a == 3) {
        native_fn_ov001_02204590(native_fn_ov001_02202360(0) + 0x18, 0x7B);
    }
    native_fn_ov001_021feeb4();
    return 0U;
}
