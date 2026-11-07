#include "context.h"
void native_main_0209c4c8 (GT2Socket socket)
{

    stLastSocketError = GOAGetLastError(gt2GetSocketSOCKET(socket));

    DWC_Printf(DWC_REPORTFLAG_ERROR, "Socket fatal error! (%d)\n",
               stLastSocketError);

    DWCi_SetError(DWC_ERROR_FATAL, DWC_ECODE_SEQ_ETC + DWC_ECODE_GS_GT2 + DWC_ECODE_TYPE_SO_SOCKET);

    stpDwcCnt->gt2Socket = NULL;
}
