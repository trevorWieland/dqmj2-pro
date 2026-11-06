#include "native_os_context.h"
void native_arm7_wram_037fbdec(OSThread *thread)
{
    OSThread *t = OSi_ThreadInfo.list;
    OSThread *pre = NULL;

    while(t && t->priority < thread->priority)
    {
        pre = t;
        t = t->next;
    }

    if (!pre)
    {
        thread->next = OSi_ThreadInfo.list;
        OSi_ThreadInfo.list = thread;
    }
    else
    {
        thread->next = pre->next;
        pre->next = thread;
    }
}
