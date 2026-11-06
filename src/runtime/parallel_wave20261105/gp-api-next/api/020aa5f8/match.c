#include "context.h"
GPResult native_main_020aa5f8(
  GPConnection * connection,
  GPEnum status,
  const char statusString[GP_STATUS_STRING_LEN],
  const char locationString[GP_LOCATION_STRING_LEN]
)
{
	char statusStringFixed[GP_STATUS_STRING_LEN];
	char locationStringFixed[GP_LOCATION_STRING_LEN];
	GPIConnection * iconnection;
	int i;

	
	
	if((connection == NULL) || (*connection == NULL))
		return GP_PARAMETER_ERROR;

	
	
	iconnection = (GPIConnection *)*connection;

	
	
	if(iconnection->simulation)
		return GP_NO_ERROR;

	
	
	if(iconnection->connectState == GPI_DISCONNECTED)
		Error(connection, GP_PARAMETER_ERROR, native_data_020e0440);

	
	
	if(statusString == NULL)
		Error(connection, GP_PARAMETER_ERROR, native_data_020e04dc);
	if(locationString == NULL)
		Error(connection, GP_PARAMETER_ERROR, native_data_020e04f4);

	
	
	strzcpy(statusStringFixed, statusString, GP_STATUS_STRING_LEN);
	for(i = 0 ; statusStringFixed[i] ; i++)
		if(statusStringFixed[i] == '\\')
			statusStringFixed[i] = '/';
	strzcpy(locationStringFixed, locationString, GP_LOCATION_STRING_LEN);
	for(i = 0 ; locationStringFixed[i] ; i++)
		if(locationStringFixed[i] == '\\')
			locationStringFixed[i] = '/';

	
	
	if((status == iconnection->lastStatusState) &&
	   (strcmp(statusStringFixed, iconnection->lastStatusString) == 0) &&
	   (strcmp(locationStringFixed, iconnection->lastLocationString) == 0))
	{
		return GP_NO_ERROR;
	}

	
	
	iconnection->lastStatusState = status;
#ifndef GSI_UNICODE
	strzcpy(iconnection->lastStatusString, statusStringFixed, GP_STATUS_STRING_LEN);
	strzcpy(iconnection->lastLocationString, locationStringFixed, GP_LOCATION_STRING_LEN);
#else
	UTF8ToUCS2StringLen(iconnection->lastStatusString, iconnection->lastStatusString_W, GP_STATUS_STRING_LEN);
	UTF8ToUCS2StringLen(iconnection->lastStatusString, iconnection->lastLocationString_W, GP_LOCATION_STRING_LEN);
#endif

	
	
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e050c);
	gpiAppendIntToBuffer(connection, &iconnection->outputBuffer, status);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e048c);
	gpiAppendIntToBuffer(connection, &iconnection->outputBuffer, iconnection->sessKey);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0518);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, statusStringFixed);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0528);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, locationStringFixed);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e04b4);

	return GP_NO_ERROR;
}
