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
extern u8 native_data_ov006_0221c008[];
/* ov006 row 0x021F2390: 16 bytes.
 *
 * ov006_context_byte_16_021f2390: Returns the signed byte at +0x16 of the context pointed to by 0x0221C008.
 *
 * Evidence: Body is a single dereference through the global at 0x0221C008.
 * Touches: global 0x0221C008 -> context +0x16 (s8).
 * Remaining unknowns: The context type and the field's meaning are not established.
 *
 * The address stays in the symbol and file name because the measurement pairs a
 * compiled symbol to the private ledger row by its eight-hex address; removing
 * it would silently unmatch the row under the pinned private ledger.
 */
u32 ov006_context_byte_16_021f2390(void) {
    return (u32) M2C_FIELD(*(u32 *)native_data_ov006_0221c008, s8 *, 0x16);
}
