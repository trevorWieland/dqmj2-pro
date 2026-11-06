#include "context.h"
GPResult native_main_0209f724 (void)
{
    char valueStr[12], keyValueStr[32];
    if (native_fn_020a3d70()->qr2MatchType != DWC_MATCH_TYPE_SC_SV) return GP_NO_ERROR;
    (void)native_fn_020061ac(valueStr, sizeof(valueStr), native_data_020e01a4, native_fn_020a3d70()->qr2NumEntry + 1);
    (void)native_fn_0209b26c(DWC_GP_SSTR_KEY_MATCH_SC_MAX, valueStr, keyValueStr, '/');
    (void)native_fn_020061ac(valueStr, sizeof(valueStr), native_data_020e01a4, native_fn_020a3d70()->gt2NumConnection + 1);
    (void)native_fn_0209b294(DWC_GP_SSTR_KEY_MATCH_SC_NUM, valueStr, keyValueStr, '/');
    (void)native_fn_020061ac(valueStr, sizeof(valueStr), native_data_020e01a4, DWC_MATCHING_VERSION);
    (void)native_fn_0209b294(DWC_GP_SSTR_KEY_MATCH_VERSION, valueStr, keyValueStr, '/');
    return native_fn_0209d1c8(DWC_STATUS_MATCH_SC_SV, keyValueStr, NULL);
}
