/* ov001 row 0x021F14A4: 28 bytes.
 *
 * ov001_clear_state_flag4_021f14a4: Clears bit 2 (value 4) in the ov001 state object's +0x18 word and returns the new word.
 *
 * Evidence: Body: state = *(u32 **)(0x02238F58 + 4); word = state[6] & ~4; state[6] = word; return word. 021F1354 sets the same bit and guards on it.
 * Touches: ov001 global 0x02238F58 -> pointer +4 -> word +0x18 (bit 2).
 * Remaining unknowns: The bit's game-level meaning (menu open? transition?) is not established.
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
extern u8 native_data_ov001_02238f58[];
u32 ov001_clear_state_flag4_021f14a4(void) {
    u32 temp_r0;

    temp_r0 = M2C_FIELD(M2C_FIELD(native_data_ov001_02238f58, void **, 4), u32 *, 0x18) & ~4;
    M2C_FIELD(M2C_FIELD(native_data_ov001_02238f58, void **, 4), u32 *, 0x18) = temp_r0;
    return temp_r0;
}
