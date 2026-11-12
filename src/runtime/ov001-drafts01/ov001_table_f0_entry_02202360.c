/* ov001 row 0x02202360: 20 bytes.
 *
 * ov001_table_f0_entry_02202360: Returns the address of entry index in the 0xF0-stride table at 0x0223A25C.
 *
 * Evidence: Body: (0xF0 * index) + 0x0223A25C; callers use the result as a record base.
 * Touches: ov001 table 0x0223A25C, stride 0xF0.
 * Remaining unknowns: The table's row schema is not established.
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
extern u8 native_data_ov001_0223a25c[];
u32 ov001_table_f0_entry_02202360(s32 index) {
    return (0xF0 * index) + (s32) native_data_ov001_0223a25c;
}
