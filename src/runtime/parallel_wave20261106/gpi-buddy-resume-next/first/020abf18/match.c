#include "context.h"
GPResult
native_main_020abf18(
  GPConnection * connection,
  int profileid,
  int type,
  const char * message
)
{
	char buffer[3501];
	GPIConnection * iconnection = (GPIConnection*)*connection;

	
	
	strzcpy(buffer, message, sizeof(buffer));

	
	
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0624);
	gpiAppendIntToBuffer(connection, &iconnection->outputBuffer, type);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e05f8);
	gpiAppendIntToBuffer(connection, &iconnection->outputBuffer, iconnection->sessKey);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0760);
	gpiAppendIntToBuffer(connection, &iconnection->outputBuffer, profileid);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e0678);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, buffer);
	gpiAppendStringToBuffer(connection, &iconnection->outputBuffer, native_data_020e061c);

	return GP_NO_ERROR;
}
