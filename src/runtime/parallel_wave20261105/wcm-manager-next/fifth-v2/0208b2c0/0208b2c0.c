#include "context.h"
WCMApList * native_main_0208b2c0 (void)
{
    WCMWork * w = native_fn_0208a31c();
    WCMApListHeader * pHeader = (WCMApListHeader *) (w->config.pbdbuffer);
    WCMApList * p = NULL;
    if ((pHeader != NULL) && (w->config.nbdbuffer > sizeof(WCMApListHeader))) {
        u32 maxBlock = (w->config.nbdbuffer - sizeof(WCMApListHeader)) / sizeof(WCMApList);
        if (maxBlock > 0) {
            s32 i;
            if (maxBlock > pHeader->count) {
                for (i = 0; i < maxBlock; i++) {
                    p = (WCMApList *) ((u32) pHeader + sizeof(WCMApListHeader) + (i * sizeof(WCMApList)));
                    if (p->state == WCM_APLIST_BLOCK_EMPTY) {
                        break;
                    }
                }
                if (i < maxBlock) {
                    p->state = WCM_APLIST_BLOCK_OCCUPY;
                    p->index = pHeader->count;
                    p->next = NULL;
                    p->previous = pHeader->tail;
                    pHeader->tail = p;
                    if (p->previous) {
                        ((WCMApList *) (p->previous))->next = p;
                    } else {
                        pHeader->head = p;
                    }
                    pHeader->count++;
                }
            }
        }
    }
    return p;
}
