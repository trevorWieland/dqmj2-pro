#include "context.h"
void native_main_0209d8f0 (GPConnection * connection, GPGetInfoResponseArg * arg, void * param)
{
#pragma unused(param)
    char userName[21];
    char gamecode_str[5];
    unsigned int gamecode;
    GPResult gpResult;
    int i;
    BOOL confirm = FALSE;

    if (arg->result != GP_NO_ERROR) {
        DWC_Printf(DWC_REPORTFLAG_LOGIN, " ERROR: GetInfo Req. why?" "?" "? : %d\n", arg->result);
        return;
    }

    DWC_Printf(DWC_REPORTFLAG_DEBUG,
               "GetInfo Req: profileID %u, lastname '%s'.\n",
               arg->profile, arg->lastname);

    for (i = 0; i < stpFriendCnt->friendListLen; i++) {
        if (DWC_GetFriendDataType(&stpFriendCnt->friendList[i]) == DWC_FRIENDDATA_LOGIN_ID) {
            DWC_LoginIdToUserName(DWCi_GetUserData(),
                                  &stpFriendCnt->friendList[i],
                                  userName);

            if (strcmp(userName, arg->lastname) == 0) {
                gpResult = gpAuthBuddyRequest(connection, arg->profile);
                DWC_SetGsProfileId(&stpFriendCnt->friendList[i], arg->profile);
                native_fn_02096e08(&stpFriendCnt->friendList[i], TRUE);
                if (native_fn_02096d04(&stpFriendCnt->friendList[i]))
                    native_fn_02096e2c(&stpFriendCnt->friendList[i], TRUE);
                confirm = TRUE;

                DWC_Printf(DWC_REPORTFLAG_UPDATE_SV,
                           "Auth buddy request from %u, friend[%d]mp.\n",
                           arg->profile, i);
            }
        } else if (DWC_GetFriendDataType(&stpFriendCnt->friendList[i]) == DWC_FRIENDDATA_GS_PROFILE_ID ||
                   DWC_GetFriendDataType(&stpFriendCnt->friendList[i]) == DWC_FRIENDDATA_FRIEND_KEY) {

            gamecode = DWCi_GetUserData()->gamecode;
            OS_SNPrintf(gamecode_str, 5, native_data_020e018c, (u8)(gamecode >> 24), (u8)(gamecode >> 16), (u8)(gamecode >> 8), (u8)gamecode);

            if (DWC_GetGsProfileId(DWCi_GetUserData(), &stpFriendCnt->friendList[i]) == arg->profile &&
                memcmp(gamecode_str, arg->lastname + DWC_ACC_USERNAME_GSBRCD_OFFSET, 4) == 0) {

                gpResult = gpAuthBuddyRequest(connection, arg->profile);
                native_fn_02096e08(&stpFriendCnt->friendList[i], TRUE);
                if (native_fn_02096d04(&stpFriendCnt->friendList[i]))
                    native_fn_02096e2c(&stpFriendCnt->friendList[i], TRUE);
                confirm = TRUE;

                DWC_Printf(DWC_REPORTFLAG_UPDATE_SV,
                           "Auth buddy request from %u, friend[%d]gs.\n",
                           arg->profile, i);
            }
        }
    }

    if (confirm) {
        (void)DWCi_GPSendBuddyRequest(arg->profile);
    } else {
        gpDenyBuddyRequest(connection, arg->profile);

        DWC_Printf(DWC_REPORTFLAG_UPDATE_SV, "Denied buddy request from %u.\n",
                   arg->profile);
    }
}
