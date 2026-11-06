#include "native_os_context.h"
void native_arm7_wram_037fbe90(void)
{
    if (OSi_RescheduleCount <= 0)
    {
        OSThreadInfo *info = &OSi_ThreadInfo;
        if (OSi_ThreadInfo.irqDepth > 0 || OS_GetProcMode() == OS_PROCMODE_IRQ)
        {
            info->isNeedRescheduling = TRUE;
        }
        else
        {
            OSThread *currentThread = OSi_GetCurrentThread();
            OSThread *nextThread = OS_SelectThread();

            if (currentThread == nextThread || !nextThread)
                return;

            if (currentThread->state != OS_THREAD_STATE_TERMINATED
                && OS_SaveContext(&currentThread->context))
                return;

            if (OSi_SystemCallbackInSwitchThread)
            {
                ((OSSwitchThreadCallback)OSi_SystemCallbackInSwitchThread) (currentThread, nextThread);
            }

            if (info->switchCallback)
            {
                ((OSSwitchThreadCallback)info->switchCallback) (currentThread, nextThread);
            }

            OS_SetCurrentThread(nextThread);

            OS_LoadContext(&nextThread->context);
        }
    }
}
