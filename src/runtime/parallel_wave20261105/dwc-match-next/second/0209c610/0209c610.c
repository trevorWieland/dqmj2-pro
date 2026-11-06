#include "context.h"
void native_main_0209c610(DWCError error, int errorCode)
{
    if (!stpLoginCnt || (error == DWC_ERROR_NONE)) return;

    DWCi_SetError(error, errorCode);

    if (stpLoginCnt->callback != NULL) {
        stpLoginCnt->callback(error, 0, stpLoginCnt->param);
    }

    DWCi_CloseLogin();
}