#include "context.h"
void native_main_0209da68 (GPConnection * connection, GPGetInfoResponseArg * arg, void * param)
{
#pragma unused(connection)
#pragma unused(param)
    char userName[21];
    int index;
    int i;
    BOOL listChanged = FALSE;
    BOOL alreadyBuddy = FALSE;

    if (arg->result != GP_NO_ERROR) {
        DWC_Printf(DWC_REPORTFLAG_LOGIN, " ERROR: GetInfo Auth. why?" "?" "? : %d\n", arg->result);
        return;
    }

    DWC_Printf(DWC_REPORTFLAG_DEBUG,
               "GetInfo Auth: profileID %u, lastname '%s'.\n",
               arg->profile, arg->lastname);

    for (i = 0; i < stpFriendCnt->friendListLen; i++) {
        if (DWC_GetFriendDataType(&stpFriendCnt->friendList[i]) == DWC_FRIENDDATA_LOGIN_ID) {

            DWC_LoginIdToUserName(DWCi_GetUserData(),
                                  &stpFriendCnt->friendList[i],
                                  userName);

            if (strcmp(userName, arg->lastname) == 0) {
                DWC_SetGsProfileId(&stpFriendCnt->friendList[i], arg->profile);
                DWCi_SetBuddyFriendData(&stpFriendCnt->friendList[i]);
                if (native_fn_02096d04(&stpFriendCnt->friendList[i]))
                    native_fn_02096e2c(&stpFriendCnt->friendList[i], TRUE);
                listChanged = TRUE;

                DWC_Printf(DWC_REPORTFLAG_UPDATE_SV,
                           "Established buddy with %u, friend[%d]mp.\n",
                           arg->profile, i);

            }
        } else if (DWC_GetFriendDataType(&stpFriendCnt->friendList[i]) == DWC_FRIENDDATA_GS_PROFILE_ID ||
                   DWC_GetFriendDataType(&stpFriendCnt->friendList[i]) == DWC_FRIENDDATA_FRIEND_KEY) {

            if (DWC_GetGsProfileId(DWCi_GetUserData(), &stpFriendCnt->friendList[i]) == arg->profile) {
                if (DWC_IsBuddyFriendData(&stpFriendCnt->friendList[i]) == TRUE) {
                    DWC_Printf(DWC_REPORTFLAG_UPDATE_SV,
                               "This profile is already my friend[%d].\n", i);
                    alreadyBuddy = TRUE;
                } else {
                    DWC_SetGsProfileId(&stpFriendCnt->friendList[i], arg->profile);
                    DWCi_SetBuddyFriendData(&stpFriendCnt->friendList[i]);
                if (native_fn_02096d04(&stpFriendCnt->friendList[i]))
                    native_fn_02096e2c(&stpFriendCnt->friendList[i], TRUE);
                    listChanged = TRUE;

                    DWC_Printf(DWC_REPORTFLAG_UPDATE_SV,
                               "Established buddy with %u, friend[%d]gs.\n",
                               arg->profile, i);
                }
            }
        }
    }

    if (listChanged) {
        index = DWCi_RefreshFriendListAll(stpFriendCnt->friendList,
                                          stpFriendCnt->friendListLen,
                                          arg->profile);

        if (!alreadyBuddy) {
            native_fn_02096e08(&stpFriendCnt->friendList[index], TRUE);
            if (native_fn_02096d04(&stpFriendCnt->friendList[index]))
                native_fn_02096e2c(&stpFriendCnt->friendList[index], TRUE);
            DWCi_CallBuddyFriendCallback(index);
        }

        stpFriendCnt->friendListChanged = 1;
    } else {
        if (!alreadyBuddy) {
            DWC_Printf(DWC_REPORTFLAG_UPDATE_SV, "Not Established buddy with %u.\n", arg->profile);
        }
    }
}
