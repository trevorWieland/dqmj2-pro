#include "context.h"
void native_main_020656f0(void)
{
    s8 i = 0;
    ResetRecord *record = native_data_021c2871;
    native_data_021c2870 = 0;
    do {
        record->ordinal0 = i;
        record->active2 = 0;
        record++;
        i++;
    } while (i < 36);
}
