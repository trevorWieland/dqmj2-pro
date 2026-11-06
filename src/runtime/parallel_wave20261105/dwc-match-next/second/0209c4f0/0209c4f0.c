#include "context.h"
void native_main_0209c4f0(DWCLoginControl * logcnt, DWCUserData * userdata, GPConnection * pGpObj, int productID, u32 gamecode, const u16 * playerName, DWCLoginCallback callback, void * param)
{
    SDK_ASSERT(logcnt);

    DWC_Printf(DWC_REPORTFLAG_LOGIN, "Login Init\n");

    stpLoginCnt = logcnt;

    MI_CpuClear8(stpLoginCnt, sizeof(DWCLoginControl));

    stpLoginCnt->pGpObj = pGpObj;
    stpLoginCnt->state = DWC_LOGIN_STATE_INIT;
    stpLoginCnt->productID = productID;
    stpLoginCnt->gamecode = gamecode;
    stpLoginCnt->playerName = playerName;
    stpLoginCnt->callback = callback;
    stpLoginCnt->param = param;

    stpLoginCnt->userdata = userdata;

    DWC_Printf(DWC_REPORTFLAG_LOGIN, "******************************************\n");
    DWC_Printf(DWC_REPORTFLAG_LOGIN, "  pseudo    UserID   : %016llx\n", DWCi_Acc_GetUserId(&userdata->pseudo));
    DWC_Printf(DWC_REPORTFLAG_LOGIN, "  pseudo    PlayerID : %08x\n", DWCi_Acc_GetPlayerId(&userdata->pseudo));
    DWC_Printf(DWC_REPORTFLAG_LOGIN, "  authentic UserID   : %016llx\n", DWCi_Acc_GetUserId(&userdata->authentic));
    DWC_Printf(DWC_REPORTFLAG_LOGIN, "  authentic PlayerID : %08x\n", DWCi_Acc_GetPlayerId(&userdata->authentic));
    DWC_Printf(DWC_REPORTFLAG_LOGIN, "******************************************\n");
}