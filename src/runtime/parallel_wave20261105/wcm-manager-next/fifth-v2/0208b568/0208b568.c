#include "context.h"
void native_main_0208b568 (WCMRecvInd callback)
{
    OSIntrMode e = native_fn_02007ff4();
    native_data_021cfcb8.recvCallback = callback;
    (void)native_fn_02008008(e);
}
