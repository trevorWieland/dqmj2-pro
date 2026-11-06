#include "context_00.h"
void native_main_020069f8 (void)
{
    OSThread * current = OS_GetCurrentThread();
    OSThread * pre = ((void *)0) ;
    OSThread * lastThread = ((void *)0) ;
    int samePriorityThread = 0;
    OSIntrMode enable = native_fn_02007ff4();
    {
        OSThread * t = native_data_main_020e33c0.field_0024.list;
        OSThread * tPre = ((void *)0) ;
        while (t) {
            if (t == current) {
                pre = tPre;
            }
            if (current->priority == t->priority) {
                lastThread = t;
                samePriorityThread++;
            }
            tPre = t;
            t = t->next;
        }
    }
    if (samePriorityThread <= 1 || lastThread == current) {
        (void)native_fn_02008008(enable);
        return;
    }
    if (!pre) {
        native_data_main_020e33c0.field_0024.list = current->next;
    } else {
        pre->next = current->next;
    }
    current->next = lastThread->next;
    lastThread->next = current;
    native_fn_020063d0();
    (void)native_fn_02008008(enable);
}
