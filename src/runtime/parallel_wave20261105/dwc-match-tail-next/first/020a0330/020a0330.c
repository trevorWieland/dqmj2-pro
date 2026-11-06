#include "context.h"
int native_main_020a0330 (char * dstMsg, const char * srcMsg, int index)
{
    const char * pSrcBegin = srcMsg;
    char * pSrcNext = NULL;
    char * pSrcEnd;
    int len;
    int i;
    pSrcEnd = strchr(pSrcBegin, '\0');
    for (i = 0; i < index; i++) {
        pSrcNext = strchr(pSrcBegin, '/');
        if (!pSrcNext) {
            return -1;
        }
        pSrcBegin = pSrcNext + 1;
    }
    pSrcNext = strchr(pSrcBegin, '/');
    if (!pSrcNext) {
        pSrcNext = pSrcEnd;
    }
    if (pSrcBegin == pSrcNext) return -1;
    len = pSrcNext - pSrcBegin;
    native_fn_02008e0c(pSrcBegin, dstMsg, (u32)len);
    dstMsg[len] = '\0';
    return len;
}
