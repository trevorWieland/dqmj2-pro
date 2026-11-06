#include "native_os_context.h"
void native_arm7_wram_037fc180(OSThread *thread, void *arg)
{
    if (OSi_StackForDestructor)
    {
        OS_InitContext(&thread->context, (u32)OSi_ExitThread, (u32)OSi_StackForDestructor);
        thread->context.r[0] = (u32)arg;
        thread->context.cpsr |= HW_PSR_DISABLE_IRQ;
        thread->state = OS_THREAD_STATE_READY;
        OS_LoadContext(&thread->context);
    }
    else
    {
        OSi_ExitThread(arg);
    }
}
