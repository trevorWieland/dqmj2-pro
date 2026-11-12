/* ov001 row 0x02223F20: 40 bytes.
 *
 * ov001_count_candidates_02223f20: Counts the non-zero entries of a three-word candidate set.
 *
 * Evidence: Body counts words[0..2] != 0; used by 02224050/02224570/02226BDC as the 'how many candidates survive' test.
 * Touches: three-word candidate block.
 * Remaining unknowns: The candidate value domain is not established.
 *
 * The address stays in the symbol and file name because the measurement pairs a
 * compiled symbol to the private ledger row by its eight-hex address; removing
 * it would silently unmatch the row under the pinned private ledger.
 */
#include "context.h"
s32 ov001_count_candidates_02223f20(u32 *candidates)
{
    s32 index;
    s32 count;
    count = 0;
    index = 0;
    do {
        if (candidates[index] != 0)
            count++;
        index++;
    } while (index < 3);
    return count;
}
