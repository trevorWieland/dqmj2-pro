/* ov001 row 0x021DB530: 72 bytes.
 *
 * ov001_mode_byte_021db530: Returns one of four mode bytes from the ov001 global 0x022355E4 in the order 3,2,0,1.
 *
 * Evidence: Switch on arg0 0..3 returns field_3/field_2/field_0/field_1 of the 4-byte global; other values return -1.
 * Touches: ov001 global 0x022355E4 (4 mode bytes).
 * Remaining unknowns: The four modes' game meaning is not established.
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
    u8 field_0;
    u8 field_1;
    u8 field_2;
    u8 field_3;
} Record_native_data_ov001_022355e4;
extern Record_native_data_ov001_022355e4 native_data_ov001_022355e4;
u32 ov001_mode_byte_021db530(u32 index) {
    if (index == 0) {
        return (u32) native_data_ov001_022355e4.field_3;
    }
    else if (index == 1) {
        return (u32) native_data_ov001_022355e4.field_2;
    }
    else if (index == 2) {
        return (u32) native_data_ov001_022355e4.field_0;
    }
    else if (index == 3) {
        return (u32) native_data_ov001_022355e4.field_1;
    }
    else {
        return -1U;
    }

}
