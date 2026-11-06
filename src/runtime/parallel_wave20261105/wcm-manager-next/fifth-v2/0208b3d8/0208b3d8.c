#include "context.h"
void native_main_0208b3d8 (WCMApList * aplist)
{
    WCMWork * w = native_fn_0208a31c();
    WCMApListHeader * pHeader = (WCMApListHeader *) (w->config.pbdbuffer);
    WCMApList * p = NULL;
    if (aplist == NULL) {
        return;
    }
    if ((pHeader != NULL) && (w->config.nbdbuffer > sizeof(WCMApListHeader))) {
        p = pHeader->head;
        while (p) {
            if (p == aplist) {
                if (p->previous) {
                    ((WCMApList *) (p->previous))->next = p->next;
                } else {
                    pHeader->head = p->next;
                }
                if (p->next) {
                    ((WCMApList *) (p->next))->previous = p->previous;
                } else {
                    pHeader->tail = p->previous;
                }
                break;
            }
            p = p->next;
        }
        aplist->next = NULL;
        aplist->previous = pHeader->tail;
        pHeader->tail = aplist;
        if (aplist->previous) {
            ((WCMApList *) (aplist->previous))->next = aplist;
        } else {
            pHeader->head = aplist;
        }
        if (p == NULL) {
            aplist->index = pHeader->count;
            pHeader->count++;
        }
    }
}
