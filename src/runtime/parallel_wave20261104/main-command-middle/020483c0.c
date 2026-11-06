#include "context.h"
void native_main_020483c0(int object)
{
    s16 index;
    for (index = 0; index < 128; ++index)
        MESSAGE_RECORDS[object].words[index] = 0;
}
