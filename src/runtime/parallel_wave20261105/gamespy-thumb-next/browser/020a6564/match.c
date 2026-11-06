#include "context.h"
void native_main_020a6564(SBServerList *serverlist, SBListCallbackReason reason, SBServer server, void *instance)
{
	ServerBrowser sb = (ServerBrowser)instance;
	switch (reason)
	{
	case slc_serveradded:
		sb->BrowserCallback(sb, sbc_serveradded, server, sb->instance);
		if ((server->state & (STATE_BASICKEYS|STATE_FULLKEYS)) == 0 || (server->state & STATE_VALIDPING) == 0) 
		{
			
			if (server->state & (STATE_PENDINGBASICQUERY|STATE_PENDINGFULLQUERY|STATE_PENDINGICMPQUERY))
				break;

			if (!sb->dontUpdate) 
			{
				int qtype;
				if (server->flags & UNSOLICITED_UDP_FLAG)
				{
					if (sb->list.state == sl_lanbrowse || sb->engine.numserverkeys == 0)
						qtype = QTYPE_FULL;
					else
						qtype = QTYPE_BASIC;
				} else
					qtype = QTYPE_ICMP; 

				if (serverlist->backendgameflags & QR2_USE_QUERY_CHALLENGE)
					native_fn_020a5afc(&sb->engine, server, 0, qtype, SBTrue);
				else
					native_fn_020a5afc(&sb->engine, server, 0, qtype, SBFalse);

			}
		}
		break; 
	case slc_serverupdated:
		if ((server->state & (STATE_BASICKEYS|STATE_FULLKEYS|STATE_VALIDPING)) == 0) 
			sb->BrowserCallback(sb, sbc_serverupdatefailed, server, sb->instance);
		else
			sb->BrowserCallback(sb, sbc_serverupdated, server, sb->instance);
		break;
	case slc_serverdeleted:
		if ((server->state & (STATE_PENDINGBASICQUERY|STATE_PENDINGFULLQUERY|STATE_PENDINGICMPQUERY)) != 0) 
			native_fn_020a5edc(&sb->engine, server);
		sb->BrowserCallback(sb, sbc_serverdeleted, server, sb->instance);
		break;
	case slc_initiallistcomplete:
		if (sb->disconnectFlag)
			native_fn_020a762c(serverlist);
		
		if (native_fn_020a8640(serverlist->servers)==0 || sb->engine.querylist.count==0)
			sb->BrowserCallback(sb, sbc_updatecomplete, NULL, sb->instance);
		break;
	case slc_disconnected:
		break; 
	case slc_queryerror:
		sb->BrowserCallback(sb, sbc_queryerror, NULL, sb->instance);
		break;
	case slc_publicipdetermined:
		native_fn_020a5ac0(&sb->engine, sb->list.mypublicip);
		break;
	case slc_serverchallengereceived:
		break;
	}
	if (server != NULL && server->publicip == sb->triggerIP && server->publicport == sb->triggerPort)
		sb->triggerIP = 0; 
}