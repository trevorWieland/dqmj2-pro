/* ov001 row 0x02226CB0: 40 bytes.
 *
 * ov001_first_candidate_02226cb0: Returns the index of the first non-zero entry of a three-word candidate set.
 *
 * Evidence: Body scans three words and returns the first non-zero index, otherwise 0; all 141 callers pass the same 12-byte candidate block.
 * Touches: three-word candidate block.
 * Remaining unknowns: The meaning of the candidate value is not established.
 *
 * The address stays in the symbol and file name because the measurement pairs a
 * compiled symbol to the private ledger row by its eight-hex address; removing
 * it would silently unmatch the row under the pinned private ledger.
 */
#include "context.h"
s32 ov001_first_candidate_02226cb0(u32 *candidates)
{
    s32 index = 0;
    do {
        if (candidates[index] != 0)
            return index;
        index++;
    } while (index < 3);
    return 0;
}
