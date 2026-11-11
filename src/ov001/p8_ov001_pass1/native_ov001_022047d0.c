#include "context.h"

/* Clear one word slot of the 12-byte record selected by the caller's index.
 * The record stride is the immediate 12 the compiler folds into the multiply. */
void native_ov001_022047d0(s32 record, s32 slot)
{
    u32 *row = (u32 *)(native_data_ov001_0223d904 + record * 12);

    row[slot] = 0;
}
