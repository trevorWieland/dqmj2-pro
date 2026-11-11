#include "context.h"
typedef struct {
    u8 unknown_0[0x208];
    u32 words[3];
} Table_ov001_0223a030;
s32 native_ov001_02203270(u32 *values)
{
    Table_ov001_0223a030 *table = (Table_ov001_0223a030 *)native_data_ov001_0223a030;
    s8 index = 0;
    do {
        if (table->words[index] != values[index])
            return 1;
        index++;
    } while (index < 3);
    return 0;
}
