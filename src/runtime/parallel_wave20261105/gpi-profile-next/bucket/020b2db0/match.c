#include "context.h"
void *native_main_020b2db0(bucketset_t set, char *name, void *value)
{
	bucket_t *pbucket = DoFind(set, name);	
	if (!pbucket)
		return NULL;
	if (pbucket->type == bt_int)
		return DoSet(pbucket, bint( (*(int *)DoGet(pbucket)) - (*(int *)value)));
	if (pbucket->type == bt_float)
		return DoSet(pbucket, bfloat( (*(double *)DoGet(pbucket)) - (*(double *)value)));
	return DoGet(pbucket);
}
