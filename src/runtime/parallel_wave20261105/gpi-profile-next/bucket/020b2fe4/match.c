#include "context.h"
void *native_main_020b2fe4(bucket_t *pbucket, void *value)
{
	if (pbucket->type == bt_int)
		pbucket->vals.ival = *(int*)value;
	else if (pbucket->type == bt_float)
		pbucket->vals.fval = *(double *)value;
	else if (pbucket->type == bt_string)
	{
		if (pbucket->vals.sval != NULL)
			gsifree(pbucket->vals.sval);
		pbucket->vals.sval = (value == NULL ? NULL : stripchars(goastrdup((char *)value)));
	}
	return DoGet(pbucket);
}
