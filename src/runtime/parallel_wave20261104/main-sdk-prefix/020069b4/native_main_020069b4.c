#include "context_00.h"
OSThread * native_main_020069b4 (void)
{
    OSThread * t = native_data_main_020e33c0.field_0024.list;
    while (t && !OS_IsThreadRunnable(t)) {
        t = t->next;
    }
    return t;
}
