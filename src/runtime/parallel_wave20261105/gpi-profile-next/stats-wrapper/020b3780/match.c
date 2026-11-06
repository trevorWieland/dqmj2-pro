#include "context.h"
double native_main_020b3780(statsgame_t game,char *name, BucketFunc func,  double value, int index)
{
	double *ret;
	DoFunc(func, game, name, &value, bt_float, ret);
	GSI_UNUSED(index);
	return *(double *)ret;
}
