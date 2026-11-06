#include "context.h"
int native_main_0209be74(u8 aid)
{
    u8 * pAidList;
    int numHost;
    int i;

    numHost = DWCi_GetAllAIDList(&pAidList);

    for (i = 0; i < numHost; i++) {
        if (pAidList[i] == aid) break;
    }

    if (i == numHost) return 0;

    return DWCi_DeleteHostByIndex(i, numHost);
}