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
extern u32 ov001_begin_state_transition_021f1354();
extern u32 ov001_select_mode_id_021f1438();
extern u32 native_fn_ov001_021f14e4();
typedef struct {
    u8 unknown_0[0x9];
    u8 field_9;
    u8 unknown_a[0x5];
    u8 field_f;
    u8 unknown_10[0xb];
    u8 field_1b;
    u8 field_1c;
    u8 unknown_1d[0x1d];
    u16 field_3a;
} Record_native_data_ov001_02238d7c;
extern Record_native_data_ov001_02238d7c native_data_ov001_02238d7c;
u32 native_ov001_021eab48(void) {
    if ((native_data_ov001_02238d7c.field_f != 0) && (native_fn_ov001_021f14e4() == 0)) {
        ov001_begin_state_transition_021f1354(native_data_ov001_02238d7c.field_1b, native_data_ov001_02238d7c.field_1c, native_data_ov001_02238d7c.field_3a, 1);
        ov001_select_mode_id_021f1438(native_data_ov001_02238d7c.field_9);
        native_data_ov001_02238d7c.field_f = 0U;
        return 1U;
    }
    return 0U;
}
