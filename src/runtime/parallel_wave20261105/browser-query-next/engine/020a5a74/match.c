#include "context.h"
void native_main_020a5a74(SBQueryEngine *engine, int maxupdates, int queryversion, SBBool lanBrowse, SBEngineCallbackFn callback, void *instance)
{
	
	
	
	if(lanBrowse == SBFalse)
	{
		if(__GSIACResult != GSIACAvailable)
		return;
	}
		SocketStartUp();
	engine->queryversion = queryversion;
	engine->maxupdates = maxupdates;
	engine->numserverkeys = 0;
	engine->ListCallback = callback;
	engine->instance = instance;
	engine->mypublicip = 0;
	engine->querysock = socket(AF_INET, SOCK_DGRAM, 0);
#if defined(SB_ICMP_SUPPORT)
	#if defined(SN_SYSTEMS)
	{
		
		sndev_set_ping_reset_type optval;
		optval.timeout_ms = MAX_QUERY_MSEC; 
		optval.reserved = 0;
		sndev_set_options(0, SN_DEV_SET_PING_RESET, &optval, sizeof(optval));
	}
	#else
	engine->icmpsock = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
	#endif
#endif
	FIFOClear(&engine->pendinglist);
	FIFOClear(&engine->querylist);
}