#include "context.h"
GPResult native_main_020aa1d0(
  GPConnection * connection,
  GPProfile profile,
  const char reason[GP_REASON_LEN]
)
{
	GPIConnection * iconnection;
	char reasonFixed[GP_REASON_LEN];
	int i;

	
	
	if((connection == NULL) || (*connection == NULL))
		return GP_PARAMETER_ERROR;

	
	
	iconnection = (GPIConnection *)*connection;

	
	
	if(iconnection->simulation)
		return GP_NO_ERROR;

	
	
	if(iconnection->connectState == GPI_DISCONNECTED)
		Error(connection, GP_PARAMETER_ERROR, native_data_020e0440);

	
	
	if(reason == NULL)
		Error(connection, GP_PARAMETER_ERROR, native_data_020e0470);

	
	
	strzcpy(reasonFixed, reason, GP_REASON_LEN);
	for(i = 0 ; reasonFixed[i] ; i++)
		if(reasonFixed[i] == '\\')
			reasonFixed[i] = '/';

	
	
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0480);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e048c);
	gpiAppendIntToBuffer(connection, &iconnection->outputBuffer, iconnection->sessKey);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0498);
	gpiAppendIntToBuffer(connection, &iconnection->outputBuffer, profile);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e04a8);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, reasonFixed);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e04b4);

	return GP_NO_ERROR;
}
