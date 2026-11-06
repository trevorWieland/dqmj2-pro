#include "context_00.h"
BOOL native_main_020167b0 (void)
{
	MBGameInfo * nextGameInfop;
	if (!native_data_main_020e68c0.field_0018.gameInfoListTop) {
		(void)native_fn_020140f8(((void *)0) , (u16 *)&native_data_main_020e68c0.field_0040, 112 , native_fn_02018908(),
		                     native_fn_0201891c(), (1 << 3) );
		return 0 ;
	}
	if (!native_data_main_020e68c0.field_0018.nowGameInfop || !native_data_main_020e68c0.field_0018.nowGameInfop->nextp) {
		nextGameInfop = native_data_main_020e68c0.field_0018.gameInfoListTop;
	} else {
		nextGameInfop = native_data_main_020e68c0.field_0018.nowGameInfop->nextp;
	}
	native_data_main_020e68c0.field_0018.nowGameInfop = nextGameInfop;
	native_fn_02016700();
	native_data_main_020e68c0.field_0018.seqNoVolat = native_data_main_020e68c0.field_0018.nowGameInfop->seqNoVolat;
	native_data_main_020e68c0.field_0018.state = MB_BEACON_STATE_FIXED_START;
	return 1 ;
}
