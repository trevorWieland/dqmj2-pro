#include "context.h"
GPResult
native_main_020ac63c(
  GPConnection * connection,
  GPIBuffer * outputBuffer,
  char c
)
{
	int len;
	int size;
	char * output;

	assert(outputBuffer != NULL);

	
	
	len = outputBuffer->len;
	size = outputBuffer->size;
	output = outputBuffer->buffer;

	
	
	if(size == len)
	{
		size += GPI_READ_SIZE;
		output = (char*)gsirealloc(output, (unsigned int)size + 1);
		if(output == NULL)
			Error(connection, GP_MEMORY_ERROR, native_data_020e07c4);
	}

	
	
	output[len] = c;
	output[len + 1] = '\0';

	
	
	outputBuffer->len++;
	outputBuffer->size = size;
	outputBuffer->buffer = output;

	return GP_NO_ERROR;
}
