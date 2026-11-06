#include "context.h"
void native_main_020977cc(void *arg)
{
#pragma unused(arg)
	int retrycount = 0;
	OSTick startwait;
	DWCAuthError result_httpparse;
	BOOL getwifiinfofromflash;
	

	for(;;) {
		if(DWCauth->http->thread.activityWord108 != 0)
			OS_JoinThread(&(DWCauth->http->thread));
		

		if(DWCauth->http->error != DWCHTTP_E_FINISH) {
			DWCauth->result.returncode = 20100;


			if(DWCauth->http->error == DWCHTTP_E_ABORT) {

				DWCi_Auth_SetError(DWCAUTH_E_ABORT);

				return;
			}
						
			if(retrycount > 2) {

				if(DWCauth->http->error == DWCHTTP_E_DNSERR)
					DWCi_Auth_SetError(DWCAUTH_E_DNSERR);
				else if(DWCauth->http->error == DWCHTTP_E_CONERR)
					DWCi_Auth_SetError(DWCAUTH_E_HTTPCONERR);
				else
					DWCi_Auth_SetError(DWCAUTH_E_HTTPERR);

				return;		
			}
			

			retrycount++;
			getwifiinfofromflash = TRUE;
			goto retry;
		}

		result_httpparse = DWCi_Auth_ParseHttp();

		
		switch(result_httpparse) {
		case DWCAUTH_E_FINISH:

			DWCi_Auth_SetError(DWCAUTH_E_FINISH);
			return;
		case DWCAUTH_E_NASALREADYEXIST:


			if(retrycount > 2) {

				DWCi_Auth_SetError(DWCAUTH_E_NASALREADYEXIST);
				
				return;
			}
			
			retrycount++;
			getwifiinfofromflash = FALSE;
			goto retry;
		case DWCAUTH_E_NASACCTEXPIRE:
			DWCi_Auth_SetError(result_httpparse);
			return;
		default:

			if(retrycount >= 2) {

				
				DWCi_Auth_SetError(result_httpparse);
				return;				
			}
			
			retrycount++;
			getwifiinfofromflash = TRUE;
			goto retry;
		}
		

retry:
		startwait = OS_GetTick();

		#ifdef SDK_PORT
		OS_Sleep(5000);
		#else
		while(OS_TicksToMilliSeconds(OS_GetTick()-startwait) < DWCAUTH_RETRYWAIT) {
			OS_LockMutex(&DWCauth->mutex);
			if(DWCauth->abort == TRUE) {
				DWCauth->result.returncode = 20100;
				OS_UnlockMutex(&DWCauth->mutex);
				DWCi_Auth_SetError(DWCAUTH_E_ABORT);
				return;
			}
			OS_UnlockMutex(&DWCauth->mutex);
			OS_Sleep(5000);
		}
		#endif
		DWC_Http_Destroy(DWCauth->http);
		OS_LockMutex(&DWCauth->mutex);
		DWCauth->error = DWCi_Auth_Start(getwifiinfofromflash);
		if(DWCauth->error != DWCAUTH_E_NOERR) {
			DWCauth->result.returncode = 20100;
			OS_UnlockMutex(&DWCauth->mutex);
			return;
		}
		OS_UnlockMutex(&DWCauth->mutex);
	}
}
