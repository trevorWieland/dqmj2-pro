#include "context.h"
GPResult native_main_020af578(GPConnection *connection, DArray keys, const char *keyName, char **keyValue)
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
		*keyValue = aKeyFound->keyValue;
	}
	freeclear(aKey.keyName);
	return GP_NO_ERROR;
}
