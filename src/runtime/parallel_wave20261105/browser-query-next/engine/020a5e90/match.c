#include "context.h"
void native_main_020a5e90(SBQueryEngine *engine)
{
	if (engine->querylist.count == 0) 
		return;
	ProcessIncomingReplies(engine, SBFalse);
#ifdef SB_ICMP_SUPPORT
	ProcessIncomingReplies(engine, SBTrue);
#endif
	TimeoutOldQueries(engine);
	if (engine->pendinglist.count > 0)
		QueueNextQueries(engine);
	if (engine->querylist.count == 0) 
		engine->ListCallback(engine, qe_engineidle, NULL, engine->instance);
}