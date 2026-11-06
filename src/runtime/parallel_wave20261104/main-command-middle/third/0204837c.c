#include "context.h"
void native_main_0204837c(int record)
{
    s16 index = 0;
    MessageRecord *target = &native_data_020fbae8[record];
    do {
        target->words[index] = 0;
        ++index;
    } while (index < 128);
}
