/* ov001 row 0x021DBD30: 12 bytes.
 *
 * ov001_record_field_1f2_021dbd30: Returns the signed 16-bit field at record + 0x1F2.
 *
 * Evidence: Body is a single load; callers use it as an actor/record accessor (src/nonmatching/overlay-lane/20261101-action436/source.c:67).
 * Touches: record +0x1F2 (s16).
 * Remaining unknowns: The field's meaning is not established.
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
u32 ov001_record_field_1f2_021dbd30(void *record) {
    return (u32) M2C_FIELD(record, s16 *, 0x1F2);
}
