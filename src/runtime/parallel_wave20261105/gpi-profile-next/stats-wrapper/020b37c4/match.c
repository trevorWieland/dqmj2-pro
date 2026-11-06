#include "context.h"
char *native_main_020b37c4(statsgame_t game,char *name, BucketFunc func,  char *value, int index)
{
	char *ret;
	DoFunc(func, game, name, value, bt_string, ret);
	GSI_UNUSED(index);
	return ret;
}
