#include "context.h"
GT2Result native_main_0209bc9c (void)
{
    u16 baseport;
    GT2Result gt2Result;

    if (stpDwcCnt->gt2Socket) {
        DWC_Printf(DWC_REPORTFLAG_WARNING, "gt2Socket is already made.\n");
        return GT2Success;
    }

    baseport = (u16)(0xc000 + DWCi_GetMathRand32(0x4000));

    DWC_Printf(DWC_REPORTFLAG_MATCH_NN, "--- Private port = %d ---\n", baseport);

    gt2Result = gt2CreateSocket(&stpDwcCnt->gt2Socket,
                                gt2AddressToString(0, baseport, NULL),
                                stpDwcCnt->gt2SendBufSize,
                                stpDwcCnt->gt2RecvBufSize,
                                DWCi_GT2SocketErrorCallback);

    if (DWCi_HandleGT2Error(gt2Result)) return gt2Result;

    gt2Listen(stpDwcCnt->gt2Socket, DWCi_GT2ConnectAttemptCallback);
    gt2SetUnrecognizedMessageCallback(stpDwcCnt->gt2Socket, DWCi_GT2UnrecognizedMessageCallback);

    return gt2Result;
}
