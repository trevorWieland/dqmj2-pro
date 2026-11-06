#include "context.h"
void native_main_020a5afc(SBQueryEngine *engine, SBServer server, int addfront, int querytype, SBBool usequerychallenge)
{
	
	FIFODebugCheckAdd(&engine->pendinglist, server);
	FIFODebugCheckAdd(&engine->querylist, server);

	server->state &= (unsigned char)~(STATE_PENDINGBASICQUERY|STATE_PENDINGFULLQUERY|STATE_PENDINGICMPQUERY|STATE_PENDINGQUERYCHALLENGE|STATE_QUERYFAILED); 
	server->splitResponseBitmap = 0;
	server->querychallenge = 0;

#ifndef SB_ICMP_SUPPORT
	if (querytype == QTYPE_ICMP)
		return; 
#endif

	if (querytype == QTYPE_BASIC)
		server->state |= STATE_PENDINGBASICQUERY;
	else if (querytype == QTYPE_FULL)
		server->state |= STATE_PENDINGFULLQUERY;
	else if (querytype == QTYPE_ICMP)
		server->state |= STATE_PENDINGICMPQUERY;
	else
		return; 
		
	if (usequerychallenge && (querytype == QTYPE_FULL || querytype == QTYPE_BASIC))
		server->state |= STATE_PENDINGQUERYCHALLENGE;
	
	if (engine->querylist.count < engine->maxupdates) 
	{
		QEStartQuery(engine, server);
		return;
	}
	
	
	if (addfront)
		FIFOAddFront(&engine->pendinglist, server);
	else
		FIFOAddRear(&engine->pendinglist, server);
}