#include "context.h"
GPResult
native_main_020b0e04(
  GPConnection * connection,
  GPISearchData ** searchData,
  int type
)
{
	GPISearchData * data;

	
	
	data = (GPISearchData *)gsimalloc(sizeof(GPISearchData));
	if(data == NULL)
		Error(connection, GP_MEMORY_ERROR, native_data_020e1170);
	memset(data, 0, sizeof(GPISearchData));
	data->type = type;
	data->sock = INVALID_SOCKET;
	data->inputBuffer.buffer = NULL;
	data->inputBuffer.len = 0;
	data->inputBuffer.pos = 0;
	data->inputBuffer.size = 0;
	data->outputBuffer.len = 0;
	data->outputBuffer.pos = 0;
	data->outputBuffer.size = 4096;
	data->outputBuffer.buffer = (char *)gsimalloc((unsigned int)data->outputBuffer.size + 1);
	if(data->outputBuffer.buffer == NULL)
		Error(connection, GP_MEMORY_ERROR, native_data_020e1170);
	data->processing = GPIFalse;
	data->remove = GPIFalse;

	*searchData = data;

	return GP_NO_ERROR;
}
