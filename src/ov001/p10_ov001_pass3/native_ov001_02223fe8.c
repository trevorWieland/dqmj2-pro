/* ov001 row 0x02223FE8: 56 bytes.
 *
 * ov001_clear_free_candidate_slots_02223fe8: Clears the candidate word for every one of three records that 021DB8D0 reports as inactive.
 *
 * Evidence: Existing header comment and body: for i in 0..2, if 021DB8D0(record + i*0x440) == 0 then slots[i] = 0.
 * Touches: three 0x440-byte records; three-word candidate block.
 * Remaining unknowns: None for the mechanism; the candidate value domain remains unknown.
 *
 * The address stays in the symbol and file name because the measurement pairs a
 * compiled symbol to the private ledger row by its eight-hex address; removing
 * it would silently unmatch the row under the pinned private ledger.
 */
#include "context.h"

void ov001_clear_free_candidate_slots_02223fe8(u32 *slots, u8 *record)
{
    s32 i = 0;

    do {
        if (ov001_record_is_active_021db8d0(record) == 0)
            slots[i] = 0;
        i++;
        record += 0x440;
    } while (i < 3);
}
