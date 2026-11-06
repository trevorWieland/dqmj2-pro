#include "context.h"
void native_main_020b85d8(int keyid, const char *key)
{
	gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Misc, GSIDebugLevel_StackTrace,
		"native_main_020b85d8()\r\n");
	if (keyid < NUM_RESERVED_KEYS || keyid > MAX_REGISTERED_KEYS)
	{
		gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Misc, GSIDebugLevel_WarmError,
			"Attempted to register invalid key %d - %s\r\n", keyid, key);
		return;
	}
	gsDebugFormat(GSIDebugCat_QR2, GSIDebugType_Misc, GSIDebugLevel_Comment,
		"Registered key %d - %s\r\n", keyid, key);
	native_data_020e277c[keyid] = key;
}
