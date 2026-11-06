#include "context.h"
u32 native_main_0208e878(const char *name,u32 server,u16 transaction)
{
    u32 result;
    if(!server)return 0xffffffff;
    native_fn_0208d7c0();
    native_fn_0208d764();
    native_fn_0208d780(0,53,server);
    result=native_fn_0208e644(name,1,transaction,0,0);
    native_fn_0208d7e0();
    return result;
}
