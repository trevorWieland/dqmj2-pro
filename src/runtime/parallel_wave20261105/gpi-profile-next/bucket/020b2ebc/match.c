#include "context.h"
void *native_main_020b2ebc(bucketset_t set, char *name, void *value)
{
	bucket_t *pbucket = DoFind(set, name);	
	char *temp, *s;
	if (!pbucket)
		return NULL;
	assert(pbucket->type == bt_string);
	s = DoGet(pbucket);
	temp = (char *)gsimalloc(strlen(s) + strlen(value) + 1);
	strcpy(temp,s);
	strcat(temp, value);
	DoSet(pbucket, temp);
	gsifree(temp);
	return DoGet(pbucket);
}
