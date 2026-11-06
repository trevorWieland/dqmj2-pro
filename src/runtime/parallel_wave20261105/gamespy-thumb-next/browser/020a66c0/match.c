#include "context.h"
void native_main_020a66c0(SBQueryEnginePtr engine, SBQueryEngineCallbackReason reason, SBServer server, void *instance)
{
	ServerBrowser sb = (ServerBrowser)instance;
	switch (reason)
	{
	case qe_updatefailed:
		sb->BrowserCallback(sb, sbc_serverupdatefailed, server, sb->instance);
		break;
	case qe_updatesuccess:
		sb->BrowserCallback(sb, sbc_serverupdated, server, sb->instance);
		break;
	case qe_engineidle:
		sb->BrowserCallback(sb, sbc_updatecomplete, server, sb->instance);
		break;
	case qe_challengereceived:
		sb->BrowserCallback(sb, sbc_serverchallengereceived, server, sb->instance);
		
		return;
	}
	if (server != NULL && server->publicip == sb->triggerIP && server->publicport == sb->triggerPort)
		sb->triggerIP = 0; 
		
	GSI_UNUSED(engine);
}