#include "context.h"
int native_main_020b3720(statsgame_t game, int pnum)
{
	FIXGAME(game, pnum);
	return *(int *)ArrayNth(game->playernums,pnum);
}
