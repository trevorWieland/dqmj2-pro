#include "context.h"
void native_main_020a41dc (GT2Connection connection, int latency)
{
    if (sTransInfo->pingCallback) {
        u8 aid = DWCi_GetConnectionAID(connection);
        sTransInfo->pingCallback(latency, aid);
    }
}
