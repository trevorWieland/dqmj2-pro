#include "context.h"
u8 native_main_0209dd80 (u8 keyID, const char * keyString, const int * valueSrc)
{
    int index;

    if (!keyString || !valueSrc) return 0;

    if ((keyID >= DWC_QR2_GAME_KEY_START) &&
        stGameMatchKeys[keyID - DWC_QR2_GAME_KEY_START].keyID) {

        if ((stGameMatchKeys[keyID - DWC_QR2_GAME_KEY_START].keyStr != NULL) &&
            (strcmp(stGameMatchKeys[keyID - DWC_QR2_GAME_KEY_START].keyStr, keyString) != 0)) {

            return 0;
        }

    } else {
        keyID = DWCi_GetNewMatchKey();
        if (!keyID) return 0;
    }

    index = keyID - DWC_QR2_GAME_KEY_START;
    stGameMatchKeys[index].keyID = keyID;
    stGameMatchKeys[index].isStr = 0;
    stGameMatchKeys[index].pad = 0;

    if (stGameMatchKeys[index].keyStr)
        DWC_Free(DWC_ALLOCTYPE_BASE, stGameMatchKeys[index].keyStr, 0);

    stGameMatchKeys[index].keyStr = DWC_Alloc(DWC_ALLOCTYPE_BASE, strlen(keyString) + 1);
    if (!stGameMatchKeys[index].keyStr) {
        DWCi_StopMatching(DWC_ERROR_FATAL, DWC_ECODE_SEQ_MATCH + DWC_ECODE_TYPE_ALLOC);
        return 0;
    }

    strcpy(stGameMatchKeys[index].keyStr, keyString);

    DWC_Printf(DWC_REPORTFLAG_DEBUG,
               "DWC_AddMatchKeyInt: key='%s', value=%d\n",
               keyString, *valueSrc);

    stGameMatchKeys[index].value = valueSrc;

    qr2_register_key(keyID, stGameMatchKeys[index].keyStr);
    return keyID;
}
