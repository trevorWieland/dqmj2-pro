#include "context.h"
void *native_main_020b2f0c(bucketset_t set, char *name, void *value)
{
	bucket_t *pbucket = DoFind(set, name);	
	if (!pbucket)
		return NULL;
	if (pbucket->type == bt_int)
		return DoSet(pbucket, bint( AVG((*(int *)DoGet(pbucket)), (*(int *)value), pbucket->nvals)));
	if (pbucket->type == bt_float)
		return DoSet(pbucket, bfloat( AVG((*(double *)DoGet(pbucket)), (*(double *)value), pbucket->nvals)));
	return DoGet(pbucket);
}
