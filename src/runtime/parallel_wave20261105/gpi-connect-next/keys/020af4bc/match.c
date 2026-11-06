#include "context.h"
GPResult native_main_020af4bc(GPConnection *connection, DArray keys, const char *theKeyName, const char *theKeyValue)
{
	GPIKey aKey;
	GS_ASSERT(keys);
	GS_ASSERT(theKeyName);
	GS_ASSERT(theKeyValue);

	if (!theKeyName)
		Error(connection, GP_PARAMETER_ERROR, native_data_020e0f64);
	if (!theKeyValue)
		Error(connection, GP_PARAMETER_ERROR, native_data_020e0f78);

	aKey.keyName = goastrdup(theKeyName);
	aKey.keyValue = goastrdup(theKeyValue);

	ArrayInsertSorted(keys, &aKey, gpiStatusInfoKeyCompFunc);

	return GP_NO_ERROR;
}
