#include "context.h"
GPResult
native_main_020acae0(
  GPConnection * connection,
  GPIBuffer * inputBuffer,
  char ** message,
  int * type,
  int * plen
)
{
	char * str;
	int len;
	char intValue[16];
	*message = NULL;
	if(inputBuffer->len < 5)
		return GP_NO_ERROR;
	str = strchr(inputBuffer->buffer, '\n');
	if(str != NULL)
	{
		if(strncmp(str - 5, native_data_020e082c, 5) != 0)
			return GP_NETWORK_ERROR;
		*str = '\0';
		if(!gpiValueForKey(inputBuffer->buffer, native_data_020e0834, intValue, sizeof(intValue)))
			return GP_NETWORK_ERROR;
		*type = atoi(intValue);
		if(!gpiValueForKey(inputBuffer->buffer, native_data_020e0838, intValue, sizeof(intValue)))
			return GP_NETWORK_ERROR;
		len = atoi(intValue);
		len++;
		if(inputBuffer->len > ((str - inputBuffer->buffer) + len))
		{
			if(str[len] != '\0')
				return GP_NETWORK_ERROR;
			*message = &str[1];
			*plen = (len - 1);
			inputBuffer->pos = ((str - inputBuffer->buffer) + len + 1);
		}
		else
		{
			*str = '\n';
		}
	}
	GSI_UNUSED(connection);
	return GP_NO_ERROR;
}
