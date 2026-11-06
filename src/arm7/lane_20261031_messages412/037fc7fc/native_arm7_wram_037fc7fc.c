#include "native_os_context.h"
BOOL native_arm7_wram_037fc7fc(OSMessageQueue *mq, OSMessage *msg, s32 flags)
{
    OSIntrMode enabled = OS_DisableInterrupts();

    while (mq->usedCount == 0)
    {
        if (!(flags & OS_MESSAGE_BLOCK))
        {
            (void)OS_RestoreInterrupts(enabled);
            return FALSE;
        }
        else
        {
            OS_SleepThread(&mq->queueReceive);
        }
    }

    if (msg != NULL)
    {
        *msg = mq->msgArray[mq->firstIndex];
    }

    (void)OS_RestoreInterrupts(enabled);
    return TRUE;
}
