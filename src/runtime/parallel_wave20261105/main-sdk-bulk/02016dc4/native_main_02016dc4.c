#include "context_00.h"
void native_main_02016dc4 (void * arg)
{
    native_data_main_020ec360.field_0008->mbIsStarted = 0;
    native_data_main_020ec360.field_000c->isMbInitialized = 0;
    if (native_data_main_020ec360.field_0008->callback) {
        native_data_main_020ec360.field_0008->callback(17 , arg);
    }
}
