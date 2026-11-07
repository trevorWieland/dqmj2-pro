#include "context.h"
int native_main_020a2b98 (SBServer server)
{
    if (SBServerGetIntValue(server, native_data_020e02b8, -1) == -1)
        return 0;

    if (SBServerGetIntValue(server, native_data_020e02c4, -1) == -1)
        return 0;

    if (SBServerGetIntValue(server, native_data_020e01fc, -1) == -1)
        return 0;
    
    if (SBServerGetIntValue(server, native_data_020e0208, -1) == -1) {
        if (SBServerGetIntValue(server, native_data_020e0208, 0) == 0) return 0;
    }
    
    if (SBServerGetIntValue(server, native_data_020e0214, -1) == -1) return 0;
    return SBServerGetIntValue(server, native_data_020e01f4, 0);
}
