/* ov001 row 0x021DB8D0: 72 bytes.
 *
 * ov001_record_is_active_021db8d0: Predicate: a battle record is active and selectable.
 *
 * Evidence: Three callers treat 0 as free/skip (src/ov001/p10_ov001_pass3/ov001_clear_free_candidate_slots_02223fe8.c; src/ov001/p12_ov001_close/arm/ov001/native_ov001_02219178.c); body rejects null, +0x31C == 0, +0x1FF != 0 and child(+0x1E8)+0xAC != 0.
 * Touches: record bytes +0x31C, +0x1FF, pointer +0x1E8 -> +0xAC.
 * Remaining unknowns: Game-level meaning of +0x31C and +0x1FF is not established; the name is a state predicate, not a menu action.
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
u32 ov001_record_is_active_021db8d0(void *record) {
    u8 temp_r2;

    if (record == NULL) {
        return 0U;
    }
    temp_r2 = M2C_FIELD(record, u8 *, 0x31C);
    if (temp_r2 == 0) {
        return 0U;
    }
    if ((temp_r2 != 0) && (M2C_FIELD(record, u8 *, 0x1FF) != 0)) {
        return 0U;
    }
    if ((temp_r2 != 0) && (M2C_FIELD(M2C_FIELD(record, void **, 0x1E8), u8 *, 0xAC) != 0)) {
        return 0U;
    }
    return 1U;
}
