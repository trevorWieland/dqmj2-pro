#include "context.h"
#include "context-data.h"
DWCAuthError native_main_0209770c(BOOL getwifiinfofromflash)
{

	if(strcmp(DWCauthhttpparam.url, DWC_AUTH_NAS_URL) != 0)
		DWCauthhttpparam.ignoreca = TRUE;
	

	DWCauthhttpparam.alloc = DWCauth->param.alloc;
    DWCauthhttpparam.free = DWCauth->param.free;

	if(DWC_Http_Create(DWCauth->http, &DWCauthhttpparam) != DWCHTTP_E_NOERR)
		return DWCAUTH_E_HTTPINITERR;
	

	if(getwifiinfofromflash == TRUE)
		DWCi_BM_GetWiFiInfo(&DWC_auth_wifiinfo);
		

	DWCauth->error = DWCi_Auth_Prepare_FirstPost(DWCauth->http, DWCauth->param.gsbrcd, &DWCauth->param);
	if(DWCauth->error != DWCAUTH_E_NOERR) {
		DWC_Printf(DWC_REPORTFLAG_AUTH, "\tAuth : Failed to initialize HTTP POST packet\n");		
		return DWCAUTH_E_HTTPINITERR;
	}
	

	if(DWC_Http_FinishHeader(DWCauth->http) != DWCHTTP_E_NOERR) {
		DWC_Printf(DWC_REPORTFLAG_AUTH, "\tAuth : Failed to finalize HTTP POST packet\n");		
		return DWCAUTH_E_HTTPINITERR;
	}
	

	DWC_Printf(DWC_REPORTFLAG_AUTH, "\tAuth : Start HTTP/HTTPS communication\n");

	DWC_Http_StartThread(DWCauth->http, OS_GetThreadPriority(OS_GetCurrentThread())-1);

	return DWCAUTH_E_NOERR;
}