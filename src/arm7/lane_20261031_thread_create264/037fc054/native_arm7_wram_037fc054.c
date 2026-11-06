#include "native_os_context.h"
void native_arm7_wram_037fc054(OSThread *thread, void (*func) (void *), void *arg, void *stack, u32 stackSize, u32 prio)
{
    OSIntrMode enable = OS_DisableInterrupts();

    s32 index = OSi_GetUnusedThreadId();

    thread->priority = prio;
    thread->id = (u32)index;
    thread->state = OS_THREAD_STATE_WAITING;

    thread->profiler = NULL;

    OSi_InsertThreadToList(thread);

    thread->stackBottom = (u32)stack;
    thread->stackTop = (u32)stack - stackSize;
    thread->stackWarningOffset = 0;

    *(u32 *)(thread->stackBottom - sizeof(u32)) = 0xd73bfdf7UL;
    *(u32 *)thread->stackTop = 0xfbdd37bbUL;

    OS_InitThreadQueue(&thread->joinQueue);

    OS_InitContext(&thread->context, (u32)func, (u32)stack - 4);

    thread->context.r[0] = (u32)arg;
    thread->context.lr = (u32)OS_ExitThread;

    MI_CpuClear32((void *)((u32)stack - stackSize + 4), stackSize - 8);

    thread->mutex = NULL;
    thread->mutexQueue.head = NULL;
    thread->mutexQueue.tail = NULL;

    OS_SetThreadDestructor(thread, NULL);

    thread->queue = NULL;
    thread->link.prev = thread->link.next = NULL;

    MI_CpuClear32(&thread->specific[0], sizeof(void *) * OS_THREAD_SPECIFIC_MAX);

    thread->alarmForSleep = NULL;

    (void)OS_RestoreInterrupts(enable);
}
