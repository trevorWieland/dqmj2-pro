#include "context.h"
void *native_main_020b2ce8(bucketset_t set, char *name, BucketType type, void *initialvalue)
{
	bucket_t bucket;
	if (set == NULL)
		set = g_buckets;
	assert(set);
	bucket.name = goastrdup(name);
	bucket.type = type;
	bucket.vals.sval = NULL;
	bucket.nvals = 1;
	DoSet(&bucket, initialvalue);
	TableEnter(set->buckets,&bucket);
	return DoGet(DoFind(set, name));
}
