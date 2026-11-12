/* ov001 row 0x021DB438: 124 bytes.
 *
 * ov001_side_slot_record_021db438: Returns the 0x440-byte record for one of four sides and one of three slots.
 *
 * Evidence: Four tables (0x02236F6C, 0x022362AC, 0x022355EC, 0x02237C2C) selected by arg0 0..3, stride 0x440, arg1 < 3; callers pass side 0/1 and slot 0..2 (src/nonmatching/overlay-lane/20261101-action436/source.c:59).
 * Touches: four 3-record tables at 0x022355EC..0x02237C2C; record stride 0x440.
 * Remaining unknowns: Which four game sides the tables represent (player, enemy, ally, neutral?) is not proven.
 *
 * The address stays in the symbol and file name because the measurement pairs a
 * compiled symbol to the private ledger row by its eight-hex address; removing
 * it would silently unmatch the row under the pinned private ledger.
 */
#define NULL ((void *)0)
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
extern u8 native_data_ov001_022355ec[];
extern u8 native_data_ov001_022362ac[];
extern u8 native_data_ov001_02236f6c[];
extern u8 native_data_ov001_02237c2c[];
u32 ov001_side_slot_record_021db438(s32 side, u32 slot) {
    void *var_r2;

    var_r2 = NULL;
    if (slot < 3U) {
        if (side == 0) {
            var_r2 = native_data_ov001_02236f6c + (slot * 0x440);
        }
        else if (side == 1) {
            var_r2 = native_data_ov001_022362ac + (slot * 0x440);
        }
        else if (side == 2) {
            var_r2 = native_data_ov001_022355ec + (slot * 0x440);
        }
        else if (side == 3) {
            var_r2 = native_data_ov001_02237c2c + (slot * 0x440);
        }

    }
    return (u32) var_r2;
}
