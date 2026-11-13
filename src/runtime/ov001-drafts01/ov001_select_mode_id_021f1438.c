/* ov001 row 0x021F1438: 108 bytes.
 *
 * ov001_select_mode_id_021f1438: Maps modes 0/1/2 to service ids 4/5/6 and forwards every other value unchanged.
 *
 * Evidence: Switch on arg0: 0 -> 02085320(state->field_4, 0, 4), 1 -> 5, 2 -> 6, default returns the input.
 * Touches: ov001 state 0x02238F58 -> +4; service 0x02085320.
 * Remaining unknowns: The service's id space and the state pointer's type are not established.
 *
 * The address stays in the symbol and file name because the measurement pairs a
 * compiled symbol to the private ledger row by its eight-hex address; removing
 * it would silently unmatch the row under the pinned private ledger.
 */
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
extern u32 native_fn_02085320();
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
} Record_native_data_ov001_02238f58;
extern Record_native_data_ov001_02238f58 native_data_ov001_02238f58;
u32 ov001_select_mode_id_021f1438(u32 mode) {
    switch (mode) {
    default:
        return mode;
    case 0:
        return native_fn_02085320(native_data_ov001_02238f58.field_4, 0, 4);
    case 1:
        return native_fn_02085320(native_data_ov001_02238f58.field_4, 0, 5);
    case 2:
        return native_fn_02085320(native_data_ov001_02238f58.field_4, 0, 6);
    }
}
