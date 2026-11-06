#include "context.h"
int native_main_0209b26c (const char * key, const char * value, char * string, char separator)
{
    SDK_ASSERT(key && value);
    native_fn_020061ac(string, DWC_COMMONSTR_MAX_KEY_VALUE_LEN,
                native_data_020e0160,
                separator, key, separator, value);
    return (int)strlen(string);
}
