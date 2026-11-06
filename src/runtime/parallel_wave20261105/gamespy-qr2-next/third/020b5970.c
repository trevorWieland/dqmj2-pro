#include "context.h"
int native_main_020b5970(const void * elem, int numBuckets)
{
	GT2Connection connection = *(GT2Connection *)elem;
	return (int)(((connection->ip * connection->port)) % numBuckets);
}
