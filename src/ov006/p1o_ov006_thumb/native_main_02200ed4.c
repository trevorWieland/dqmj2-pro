#include "context.h"

extern u8 native_data_0221c160[];
extern void native_fn_02018604(void);

/* Hand off when the record's first halfword is 4 and its +2/+0xc halfwords
   match. */
void native_main_02200ed4(void)
{
    u16 *record = (u16 *)*(u32 **)native_data_0221c160;

    if (record[0] == 4 && record[1] == record[6])
        native_fn_02018604();
}
