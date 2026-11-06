#include "context.h"
int native_main_020a601c(Server *server,const char *key,int fallback)
{
    const char *s,*s2;
    if(server==0)return fallback;
    if(native_fn_0201d800(key,native_data_020e0318)==0)return native_fn_020a64d0(server);
    s=native_fn_020a5fe4(server,key,0);
    if(s==0)return fallback;
    s2=(*s!='-')?s:s+1;
    if(!digit((u8)*s2))return fallback;
    return native_fn_0201f274(s);
}
