#include "context_00.h"
void native_main_020189b0 (u16 apiid, int errcode)
{
    u16 arg[2];
    if (errcode != WM_ERRCODE_OPERATING && errcode != WM_ERRCODE_SUCCESS) {
        arg[0] = apiid;
        arg[1] = (u16)errcode;
        native_data_main_020ec360.field_0008->callback(255 , arg);
    }
}
