#include "context.h"
void
native_main_020b2a38(
  char * dest,
  const char * src,
  size_t len
)
{
	assert(dest != NULL);
	assert(src != NULL);

	strncpy(dest, src, len);
	dest[len - 1] = '\0';
}
