#include "context.h"
void native_main_0204983c(int first, int second)
{
    s8 index = 0;
    do {
        Entry *entry = native_fn_02049aa8(index);
        if (entry->link && entry->link->resource && entry->field4 == first && entry->field5 == second) {
            native_fn_02049898(entry);
        }
        ++index;
    } while (index < 36);
}
