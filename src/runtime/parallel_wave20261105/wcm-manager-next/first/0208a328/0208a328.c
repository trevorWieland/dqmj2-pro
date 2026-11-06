#include "context.h"
void native_main_0208a328(WCMConfig* config, WCMNotify notify)
{
    if (config == NULL)
    {
        native_data_021cfcb4->config.dmano = 3;
        native_data_021cfcb4->config.pbdbuffer = NULL;
        native_data_021cfcb4->config.nbdbuffer = 0;
        native_data_021cfcb4->config.nbdmode = 0;
    }
    else
    {
        if (config->dmano &~(0x03))
        {
            WCMi_Warning(wcmWarningText_IllegalParam, "config->dmano");
        }
        native_data_021cfcb4->config.dmano = (config->dmano & 0x03);
        if ((((4 - ((u32) (config->pbdbuffer) & 0x03)) % 4) + sizeof(WCMApListHeader)) > config->nbdbuffer)
        {
            native_data_021cfcb4->config.pbdbuffer = NULL;
            native_data_021cfcb4->config.nbdbuffer = 0;
        }
        else
        {
            native_data_021cfcb4->config.pbdbuffer = (void*)WCM_ROUNDUP4((u32) (config->pbdbuffer));
            native_data_021cfcb4->config.nbdbuffer = config->nbdbuffer - (s32) ((4 - ((u32) (config->pbdbuffer) & 0x03)) % 4);
            MI_CpuClear8(native_data_021cfcb4->config.pbdbuffer, (u32) (native_data_021cfcb4->config.nbdbuffer));
        }
        native_data_021cfcb4->config.nbdmode = config->nbdmode;
    }
    native_data_021cfcb4->notify = notify;
}
