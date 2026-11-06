#include "context.h"
int native_main_020a1908 (void)
{
    int result;
    int i;
    for (i = 1; i <= native_fn_020a3d70()->gt2NumConnection; i++) {
        result = native_fn_020a00ac(DWC_MATCH_COMMAND_CLOSE_LINK,
                                       native_fn_020a3d70()->sbPidList[i],
                                       native_fn_020a3d70()->qr2IPList[i],
                                       native_fn_020a3d70()->qr2PortList[i],
                                       native_fn_020a3d70()->svDataBak,
                                       (int)(native_fn_020a3d70()->svDataBak[0] + 1));
        if (result) return result;
    }
    native_fn_020a3d70()->qr2IsReserved = 0;
    native_fn_020a3d70()->qr2Reservation = 0;
    native_fn_020a3d70()->closeState = DWC_MATCH_CLOSE_STATE_CHANGE_TO_CLIENT;
    native_fn_020b4540(*native_fn_020a3d70()->pGt2Socket);
    native_fn_020a3d70()->closeState = DWC_MATCH_CLOSE_STATE_INIT;
    DWC_Printf(DWC_REPORTFLAG_MATCH_NN,
               "Closed all connections. Begin NN to %u\n",
               native_fn_020a3d70()->reqProfileID);
    return 0;
}
