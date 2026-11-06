#include "context.h"
u8 native_main_0209cbd4(const DWCFriendData * friendData, u8 * maxEntry, u8 * numEntry, char * statusString)
{
    char valueStr[4];
    int len;
    GPBuddyStatus status;

    if (DWCi_GetFriendBuddyStatus(friendData, &status)) {
        if (status.status == DWC_STATUS_MATCH_SC_SV) {
            if (maxEntry) {
                len = DWC_GetCommonValueString(DWC_GP_SSTR_KEY_MATCH_SC_MAX,
                                               valueStr,
                                               status.statusString, '/');
                if (len > 0) *maxEntry = (u8)strtoul(valueStr, NULL, 10);
                else *maxEntry = 0;
            }

            if (numEntry) {
                len = DWC_GetCommonValueString(DWC_GP_SSTR_KEY_MATCH_SC_NUM,
                                               valueStr,
                                               status.statusString, '/');
                if (len > 0) *numEntry = (u8)strtoul(valueStr, NULL, 10);
                else *numEntry = 0;
            }
        } else {
            if (maxEntry) *maxEntry = 0;
            if (numEntry) *numEntry = 0;
        }

        if (statusString) {
            strcpy(statusString, status.locationString);
        }

        return status.status;
    } else {
        if (maxEntry) *maxEntry = 0;
        if (numEntry) *numEntry = 0;
        return DWC_STATUS_OFFLINE;
    }
}