#include "context.h"
GPResult
native_main_020ac684(
  GPConnection * connection,
  GPIBuffer * outputBuffer,
  const char * string,
  int stringLen
)
{
	int len;
	int size;
	char * output;

	assert(string != NULL);
	assert(stringLen >= 0);
	assert(outputBuffer != NULL);

	if(!string)
		return GP_NO_ERROR;

	
	
	len = outputBuffer->len;
	size = outputBuffer->size;
	output = outputBuffer->buffer;

	
	
	if((size - len) < stringLen)
	{
		size += max(GPI_READ_SIZE, stringLen);
		output = (char*)gsirealloc(output, (unsigned int)size + 1);
		if(output == NULL)
			Error(connection, GP_MEMORY_ERROR, native_data_020e07c4);
	}

	
	
	memcpy(&output[len], string, (unsigned int)stringLen);
	output[len + stringLen] = '\0';

	
	
	outputBuffer->len += stringLen;
	outputBuffer->size = size;
	outputBuffer->buffer = output;

	return GP_NO_ERROR;
}
