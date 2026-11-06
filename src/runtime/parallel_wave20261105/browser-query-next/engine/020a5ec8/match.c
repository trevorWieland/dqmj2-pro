#include "context.h"
void native_main_020a5ec8(SBQueryEngine *engine, unsigned char keyid)
{
	if (engine->numserverkeys < MAX_QUERY_KEYS)
		engine->serverkeys[engine->numserverkeys++] = keyid;
}