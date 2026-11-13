/* ov006 row 0x021E65A4: 28 bytes.
 *
 * ov006_active_state_value_021e65a4: Returns state word +0x44 only while state word +0x40 equals 1, otherwise 0.
 *
 * Evidence: Typed access to global 0x02218D90: if field_40 != 1 return 0; return field_44.
 * Touches: ov006 global 0x02218D90 (+0x40 gate, +0x44 value).
 * Remaining unknowns: What the gated value represents is not established.
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
typedef struct {
    u8 unknown_0[0x40];
    s32 field_40;
    u32 field_44;
} Record_native_data_ov006_02218d90;
extern Record_native_data_ov006_02218d90 native_data_ov006_02218d90;
u32 ov006_active_state_value_021e65a4(void) {
    if (native_data_ov006_02218d90.field_40 != 1) {
        return 0U;
    }
    return native_data_ov006_02218d90.field_44;
}
