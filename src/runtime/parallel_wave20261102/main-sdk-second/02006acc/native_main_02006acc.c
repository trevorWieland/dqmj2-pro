#include "context_00.h"
BOOL native_main_02006acc (OSThread * thread, u32 prio)
{
    OSThread * t = native_data_main_020e33c0.field_0024.list;
    OSThread * pre = ((void *)0) ;
    OSIntrMode enable;
    ((void) 0)                  ;
    ((void) 0) ;
    enable = native_fn_02007ff4();
    while (t && t != thread) {
        pre = t;
        t = t->next;
    }
    if (!t || t == &native_data_main_020e33c0.field_0034) {
        (void)native_fn_02008008(enable);
        return 0 ;
    }
    if (t->priority != prio) {
        if (!pre) {
            native_data_main_020e33c0.field_0024.list = thread->next;
        } else {
            pre->next = thread->next;
        }
        thread->priority = prio;
        native_fn_02006328(thread);
        native_fn_020063d0();
    }
    (void)native_fn_02008008(enable);
    return 1 ;
}
