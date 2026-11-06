#include "context.h"
GPResult
native_main_020b2b90(
  GPConnection * connection,
  const char * buffer,
  int * index,
  char key[512],
  char value[512]
)
{
	int c;
	int i;
	char * start;
	assert(buffer != NULL);
	assert(key != NULL);
	assert(value != NULL);
	buffer += *index;
	start = (char *)buffer;
	if(*buffer++ != '\\')
		CallbackFatalError(connection, GP_NETWORK_ERROR, GP_PARSE, native_data_020e15e0);
	for(i = 0 ; (c = *buffer++) != '\\' ; i++)
	{
		if(c == '\0')
			CallbackFatalError(connection, GP_NETWORK_ERROR, GP_PARSE, native_data_020e15e0);
		if(i == 511)
			CallbackFatalError(connection, GP_NETWORK_ERROR, GP_PARSE, native_data_020e15e0);
		*key++ = (char)c;
	}
	*key = '\0';
	for(i = 0 ; ((c = *buffer++) != '\\') && (c != '\0') ; i++)
	{
		if(i == 511)
			CallbackFatalError(connection, GP_NETWORK_ERROR, GP_PARSE, native_data_020e15e0);
		*value++ = (char)c;
	}
	*value = '\0';
	*index += (buffer - start - 1);
	return GP_NO_ERROR;
}
