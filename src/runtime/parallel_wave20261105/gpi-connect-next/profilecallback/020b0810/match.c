#include "context.h"
int
native_main_020b0810(
  const void *arg,
  int numBuckets
)
{
	const GPIProfile * profile = (const GPIProfile *)arg;
	return (profile->profileId % numBuckets);
}
