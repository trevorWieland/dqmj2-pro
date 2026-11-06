#include "context.h"
u32 native_main_02095e9c(tagACWORK*w){if(SOC_GetHostID()!=0){CheckSetDNS(w);if(w->skipNetCheck==1)return 15;return 13;}if(((OS_GetTick()-w->timeOut)*64)/33514000>=10){w->findList[w->connectNo].state=1;return 11;}return 12;}
