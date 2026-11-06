#include "native_os_context.h"
BOOL native_arm7_wram_037fc3c0(OSThread *thread, u32 prio)
{
    OSThread *t = OSi_ThreadInfo.list;
    OSThread *pre = NULL;
    OSIntrMode enabled = OS_DisableInterrupts();

    while (t && t != thread)
    {
        pre = t;
        t = t->next;
    }

    if (!t || t == &OSi_IdleThread)
    {
        (void)OS_RestoreInterrupts(enabled);
        return FALSE;
    }

    if (t->priority != prio)
    {
        if (!pre)
        {
            OSi_ThreadInfo.list = thread->next;
        }
        else
        {
            pre->next = thread->next;
        }

        thread->priority = prio;
        OSi_InsertThreadToList(thread);

        OSi_RescheduleThread();
    }

    (void)OS_RestoreInterrupts(enabled);

    return TRUE;
}
