#include "context.h"
GPIBool
native_main_020b2a4c(
  GPConnection * connection,
  const char * input,
  GPIBool callErrorCallback
)
{
	char buffer[16];
	GPIConnection * iconnection = (GPIConnection*)*connection;
	if(strncmp(input, native_data_020e1584, 7) == 0)
	{
		if(gpiValueForKey(input, native_data_020e158c, buffer, sizeof(buffer)))
			iconnection->errorCode = (GPErrorCode)atoi(buffer);
		if(!gpiValueForKey(input, native_data_020e1594, iconnection->errorString, sizeof(iconnection->errorString)))
			iconnection->errorString[0] = '\0';
#ifdef GSI_UNICODE
		UTF8ToUCS2String(iconnection->errorString, iconnection->errorString_W);
#endif
		if(callErrorCallback)
		{
			GPIBool fatal = (GPIBool)(strstr(input, native_data_020e15a0) != NULL);
			gpiCallErrorCallback(connection, GP_SERVER_ERROR, fatal ? GP_FATAL : GP_NON_FATAL);
		}
		return GPITrue;
	}
	return GPIFalse;
}
