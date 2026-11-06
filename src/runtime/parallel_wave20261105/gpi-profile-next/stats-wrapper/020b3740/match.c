#include "context.h"
int native_main_020b3740(statsgame_t game,char *name, BucketFunc func,  int value, int index)
{
	int *ret;
	DoFunc(func, game, name, &value, bt_int, ret);
	GSI_UNUSED(index);
	return *(int *)ret;
}
