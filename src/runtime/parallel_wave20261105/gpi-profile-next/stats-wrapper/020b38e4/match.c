#include "context.h"
double native_main_020b38e4(statsgame_t game,char *name, BucketFunc func,  double value, int index)
{
	char fullname[64];
	sprintf(fullname, native_data_020e16e0,name, GetPlayerIndex(game, index));
	return ServerOpFloat(game, fullname, func, value, index);
}
