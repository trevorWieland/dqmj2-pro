#include "context.h"
GPResult native_main_020af510(GPConnection *connection, DArray keys, const char *keyName, const char *newKeyValue)
{
	GPIKey aKey;
	int anIndex;
	GS_ASSERT(keys);
	GS_ASSERT(keyName);

	if (!keyName)
		Error(connection, GP_PARAMETER_ERROR, native_data_020e0f64);

	aKey.keyName = goastrdup(keyName);
	anIndex = ArraySearch(keys, &aKey, gpiStatusInfoKeyCompFunc, 0, 1);
	if (anIndex != NOT_FOUND)
	{
		GPIKey *aKeyFound = (GPIKey *)ArrayNth(keys, anIndex);
		gsifree(aKeyFound->keyValue);
		aKeyFound->keyValue = goastrdup(newKeyValue);
	}
	freeclear(aKey.keyName);
	return GP_NO_ERROR;
}
