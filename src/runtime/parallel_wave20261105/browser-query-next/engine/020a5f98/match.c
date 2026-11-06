#include "context.h"
void native_main_020a5f98(SBServer server, const char *keyname, const char *value)
{
	SBKeyValuePair kv;
	kv.key = SBRefStr(NULL, keyname);
	kv.value = SBRefStr(NULL, value);
	TableEnter(server->keyvals, &kv);

	gsDebugFormat(GSIDebugCat_SB, GSIDebugType_Misc, GSIDebugLevel_Comment,
			"SBServerAddKeyValue added %s\\%s\r\n", keyname, value);
}