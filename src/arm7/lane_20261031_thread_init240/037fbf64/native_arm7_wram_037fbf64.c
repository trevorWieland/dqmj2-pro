#include "native_os_context.h"
void native_arm7_wram_037fbf64(void)
{
    if (OSi_IsThreadInitialized)
        return;
    OSi_IsThreadInitialized = TRUE;

    OSi_CurrentThreadPtr = &(OSi_ThreadInfo.current);

    OSi_LauncherThread.priority = OS_THREAD_LAUNCHER_PRIORITY;
    OSi_LauncherThread.id = 0;
    OSi_LauncherThread.state = OS_THREAD_STATE_READY;
    OSi_LauncherThread.next = NULL;

    OSi_LauncherThread.profiler = NULL;

    OSi_ThreadInfo.list = &OSi_LauncherThread;

    OS_SetCurrentThread(&OSi_LauncherThread);

    void *stackLo = (((s32)SDK_SYS_STACKSIZE) <= 0) ?
                    (void *)((u32)HW_WRAM - (s32)SDK_SYS_STACKSIZE) :
                    (void *)((u32)(HW_PRV_WRAM_IRQ_STACK_END - (s32)SDK_IRQ_STACKSIZE) - (s32)SDK_SYS_STACKSIZE);

    OSi_LauncherThread.stackBottom = (u32)(HW_PRV_WRAM_IRQ_STACK_END - (s32)SDK_IRQ_STACKSIZE);
    OSi_LauncherThread.stackTop = (u32)stackLo;
    OSi_LauncherThread.stackWarningOffset = 0;

    
    *(u32 *)(OSi_LauncherThread.stackBottom - sizeof(u32)) = 0xd73bfdf7UL;
    *(u32 *)OSi_LauncherThread.stackTop = 0xfbdd37bbUL;

    OS_InitThreadQueue(&OSi_LauncherThread.joinQueue);

    OSi_ThreadInfo.isNeedRescheduling = FALSE;
    OSi_ThreadInfo.irqDepth = 0;

    OS_GetSystemWork()->threadinfo_subp = &OSi_ThreadInfo;

    (void)OS_SetSwitchThreadCallback(NULL);
}
