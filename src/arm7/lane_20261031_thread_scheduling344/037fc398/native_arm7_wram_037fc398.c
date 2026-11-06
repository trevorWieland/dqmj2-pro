#include "native_os_context.h"
OSThread *native_arm7_wram_037fc398(void)
{
    OSThread *thread = OSi_ThreadInfo.list;

    while (thread && !OS_IsThreadRunnable(thread))
    {
        thread = thread->next;
    }

    return thread;
}
