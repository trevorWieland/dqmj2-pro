#include "context.h"
bucket_t *native_main_020b3048(bucketset_t set, char *name)
{
	bucket_t tbucket;
	if (set == NULL)
		set = g_buckets;
	assert(set);
	tbucket.name = name;
	return (bucket_t *)TableLookup(set->buckets,&tbucket);
}
