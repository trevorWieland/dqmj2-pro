#include "context.h"
void native_main_02097618(void)
{
    DWCAuthFree freeCallback;
    if(DWCauth == NULL)
        return;
    freeCallback = DWCauth->param.free;
    if(DWCauth->http != NULL)
        DWC_Http_Destroy(DWCauth->http);
    freeCallback((unsigned long)native_data_020deb80,DWCauth,0);
    DWCauth = NULL;
}
