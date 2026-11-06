#include "native_os_context.h"
void native_arm7_wram_037fbe4c(OSThread *thread)
{
    OSThread *t = OSi_ThreadInfo.list;
    OSThread *pre = NULL;

    while (t && t != thread)
    {
        pre = t;
        t = t-> next;
    }

    if (!pre)
    {
        OSi_ThreadInfo.list = thread->next;
    }
    else
    {
        pre->next = thread->next;
    }
}
