#include "context_00.h"
void native_main_02006388 (OSThread * thread)
{
    OSThread * t = native_data_main_020e33c0.field_0024.list;
    OSThread * pre = ((void *)0) ;
    while (t && t != thread) {
        pre = t;
        t = t->next;
    }
    ((void) 0) ;
    if (!pre) {
        native_data_main_020e33c0.field_0024.list = thread->next;
    } else {
        pre->next = thread->next;
    }
}
