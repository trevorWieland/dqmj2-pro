#include "native_os_context.h"
void native_arm7_wram_037fc2e4(OSThreadQueue *queue)
{
    OSIntrMode enabled = OS_DisableInterrupts();

    if (queue->head)
    {
        while (queue->head)
        {
            OSThread *thread = OSi_RemoveLinkFromQueue(queue);

            thread->state = OS_THREAD_STATE_READY;
            thread->queue = NULL;
            thread->link.prev = thread->link.next = NULL;
        }

        OS_InitThreadQueue(queue);
        OSi_RescheduleThread();
    }

    (void)OS_RestoreInterrupts(enabled);
}
