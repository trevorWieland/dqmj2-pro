#include "native_os_context.h"
OSThread *native_arm7_wram_037fbd64(OSThreadQueue *queue, OSThread *thread)
{
    OSThread *queueHead = queue->head;

    while (queueHead)
    {
        OSThread *next = queueHead->link.next;

        if (queueHead == thread)
        {
            OSThread *prev = queueHead->link.prev;

            if (queue->head == queueHead)
            {
                queue->head = next;
            }
            else
            {
                prev->link.next = next;
            }

            if (queue->tail == queueHead)
            {
                queue->tail = prev;
            }
            else
            {
                next->link.prev = prev;
            }

            break;
        }

        queueHead = next;
    }

    return queueHead;
}
