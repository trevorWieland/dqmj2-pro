#include "context.h"
void native_main_020a5e14(SBQueryEngine *engine)
{
	gsi_time ctime = current_time();
	while (engine->querylist.first != NULL)
	{
		if (ctime > engine->querylist.first->updatetime + MAX_QUERY_MSEC)
		{
			engine->querylist.first->flags |= STATE_QUERYFAILED;
			engine->querylist.first->updatetime = MAX_QUERY_MSEC;
			engine->querylist.first->flags  &= (unsigned char)~(STATE_PENDINGBASICQUERY|STATE_PENDINGFULLQUERY|STATE_PENDINGICMPQUERY);
			engine->ListCallback(engine, qe_updatefailed, engine->querylist.first, engine->instance);			
			FIFOGetFirst(&engine->querylist);
		} else
			break; 
	}
}