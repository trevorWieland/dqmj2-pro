#include "context.h"
u32 native_main_0208a28c(u32 option)
{
    OSIntrMode  e = native_fn_02007ff4();
    u32         filter = 0;
    u32         old_option = native_data_021cfcb4->option;
    if (native_data_021cfcb4 == NULL)
    {
        (void)native_fn_02008008(e);
        return 0;
    }
    if (option & WCM_OPTION_TEST_CHANNEL)
    {
        filter |= WCM_OPTION_FILTER_CHANNEL;
        if (!(option & WCM_OPTION_FILTER_CHANNEL))
        {
            option |= WCM_OPTION_CHANNEL_RDC;
        }
    }
    if (option & WCM_OPTION_TEST_POWER)
    {
        filter |= WCM_OPTION_FILTER_POWER;
    }
    if (option & WCM_OPTION_TEST_AUTH)
    {
        filter |= WCM_OPTION_FILTER_AUTH;
    }
    if (option & WCM_OPTION_TEST_SCANTYPE)
    {
        filter |= WCM_OPTION_FILTER_SCANTYPE;
    }
    if (option & WCM_OPTION_TEST_ROUNDSCAN)
    {
        filter |= WCM_OPTION_FILTER_ROUNDSCAN;
    }
    native_data_021cfcb4->option = (u32) ((old_option &~filter) | option);
    (void)native_fn_02008008(e);
    return old_option;
}
