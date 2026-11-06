#include "context.h"
void native_main_020975b8(void)
{
	if(DWCauth == NULL)
		return;
	
	DWC_Printf(DWC_REPORTFLAG_AUTH, "\tAuth : Aborting\n");
	
	DWC_Printf(DWC_REPORTFLAG_AUTH, "\tAuth : Locking mutex\n");
	OS_LockMutex(&DWCauth->mutex);
	DWCauth->abort = TRUE;
	OS_UnlockMutex(&DWCauth->mutex);
	DWC_Printf(DWC_REPORTFLAG_AUTH, "\tAuth : Freed mutex\n");
	

	if(DWCauth->http != NULL) {
		DWC_Printf(DWC_REPORTFLAG_AUTH, "\tAuth : Aborting Http\n");
		DWC_Http_Abort(DWCauth->http);
		DWC_Printf(DWC_REPORTFLAG_AUTH, "\tAuth : Aborting Http finished\n");		
	}
	
	DWC_Printf(DWC_REPORTFLAG_AUTH, "\tAuth : Waiting for Auth thread finish\n");
	if(DWCauth->thread.activityWord108 != 0)
		OS_JoinThread(&DWCauth->thread);
	
	DWC_Printf(DWC_REPORTFLAG_AUTH, "\tAuth : Aborted\n");
}