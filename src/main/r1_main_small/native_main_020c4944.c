#include "context.h"

extern u8 native_data_021d53b4[];
extern u8 native_data_021d53d4[];

/* Four-word block type for the 0x021d53b4 -> 0x021d53d4 copy. */
typedef struct {
    u32 word0;
    u32 word1;
    u32 word2;
    u32 word3;
} Block4;

/* Copy the four-word block at 0x021d53b4 over the block at 0x021d53d4.
   Unknowns: the two blocks' roles; the copy is an inline 16-byte assignment, not
   a call, so the source used a struct type rather than a byte loop. */
void native_main_020c4944(void)
{
    *(Block4 *)native_data_021d53d4 = *(Block4 *)native_data_021d53b4;
}
