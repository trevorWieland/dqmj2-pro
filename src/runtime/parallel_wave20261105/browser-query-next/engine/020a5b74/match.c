#include "context.h"
void native_main_020a5b74(SBQueryEngine *engine, SBServer server, char *data, int len)
{
	int i;
	int dlen;

	
	if (data[0] != 0x00 && data[0] != 0x09)
		return;

	
	data += 5;
	len -= 5;
	if (server->state & STATE_PENDINGQUERYCHALLENGE)
	{
		server->state &= (unsigned char)~(STATE_PENDINGQUERYCHALLENGE);

		if (len > 0)
		{
			server->querychallenge = (gsi_u32)atoi(data);
			FIFORemove(&engine->querylist, server); 
			QEStartQuery(engine, server); 
			engine->ListCallback(engine, qe_challengereceived, server, engine->instance);
			return;
		}
	}
	else if (server->state & STATE_PENDINGBASICQUERY)
	{
		
		for (i = 0 ; i < engine->numserverkeys ; i++)
		{
			dlen = NTSLengthSB(data, len);
			if (dlen < 0)
				break;
			
			if (!qr2_internal_is_master_only_key(qr2_registered_key_list[engine->serverkeys[i]]))
			{
				SBServerAddKeyValue(server, qr2_registered_key_list[engine->serverkeys[i]], data);
			}
			data += dlen;
			len -= dlen;
		}
		server->state |= STATE_BASICKEYS|STATE_VALIDPING;
	}
	else 
	{
		
		if (*data && strncmp(native_data_020e02f0, data, 8)==0)
		{
			SBServerParseQR2FullKeysSplit(server, data, len);
			if (server->splitResponseBitmap != 0xFF)
				return;
			server->state |= STATE_FULLKEYS|STATE_BASICKEYS|STATE_VALIDPING;
		}
		else
		{
			
			SBServerParseQR2FullKeysSingle(server, data, len);
			server->state |= STATE_FULLKEYS|STATE_BASICKEYS|STATE_VALIDPING;
		}
	}
	server->state &= (unsigned char)~(STATE_PENDINGBASICQUERY|STATE_PENDINGFULLQUERY);
	server->updatetime = current_time() - server->updatetime;
	FIFORemove(&engine->querylist, server);
	engine->ListCallback(engine, qe_updatesuccess, server, engine->instance);
}