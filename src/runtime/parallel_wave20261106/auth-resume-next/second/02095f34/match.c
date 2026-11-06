#include "context.h"
u32 native_main_02095f34(tagACWORK*w){tagACHOLD*h=DWCi_AC_GetMemPtr(1);int error=DWC_Netcheck_GetError();if(error!=0){u32 type=DWCi_ConvConnectAPType(w->connectApType);if(h->endType==type)h->errorTest=DWC_Netcheck_GetReturnCode();DWC_Netcheck_Destroy();if(error!=11){w->findList[w->connectNo].state=1;return 11;}return 15;}return 14;}
