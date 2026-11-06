#include "context.h"
GPIBool
native_main_020b2ae0(
  const char * command,
  const char * key,
  char * value,
  int len
)
{
	char delimiter;
	const char * start;
	int i;
	char c;
	assert(command != NULL);
	assert(key != NULL);
	assert(value != NULL);
	assert(len > 0);
	delimiter = key[0];
	start = strstr(command, key);
	if(start == NULL)
		return GPIFalse;
	start += strlen(key);
	len--;
	for(i = 0 ; (i < len) && ((c = start[i]) != '\0') && (c != delimiter) ; i++)
	{
		value[i] = c;
	}
	value[i] = '\0';
	return GPITrue;
}
