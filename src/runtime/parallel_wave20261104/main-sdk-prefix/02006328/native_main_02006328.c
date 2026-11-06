#include "context_00.h"
void native_main_02006328 (OSThread * thread)
{
    OSThread * t = native_data_main_020e33c0.field_0024.list;
    OSThread * pre = ((void *)0) ;
    while (t && t->priority < thread->priority) {
        pre = t;
        t = t->next;
    }
    if (!pre) {
        thread->next = native_data_main_020e33c0.field_0024.list;
        native_data_main_020e33c0.field_0024.list = thread;
    } else {
        thread->next = pre->next;
        pre->next = thread;
    }
}
