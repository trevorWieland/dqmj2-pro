#include "context.h"
void native_main_020a5cb0(SBQueryEngine *engine, SBServer server, char *data, int len)
{
	int isfinal;
	
	isfinal = (strstr(data,native_data_020e02fc) != NULL);
	SBServerParseKeyVals(server, data);
	if (isfinal)
	{
		if (server->state & STATE_PENDINGBASICQUERY)
			server->state |= STATE_BASICKEYS|STATE_VALIDPING;
		else
			server->state |= STATE_FULLKEYS|STATE_VALIDPING;
		server->state &= (unsigned char)~(STATE_PENDINGBASICQUERY|STATE_PENDINGFULLQUERY);
		server->updatetime = current_time() - server->updatetime;
		FIFORemove(&engine->querylist, server);
		engine->ListCallback(engine, qe_updatesuccess, server, engine->instance);
	}
	
	GSI_UNUSED(len);
}