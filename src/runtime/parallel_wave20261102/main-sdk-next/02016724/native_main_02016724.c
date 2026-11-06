#include "context_00.h"
void native_main_02016724 (u32 ggid, u16 tgid, u8 attribute)
{
	while (1) {
		switch (native_data_main_020e68c0.field_0018.state) {
		case MB_BEACON_STATE_STOP:
		case MB_BEACON_STATE_READY:
			if (!native_fn_020167b0()) {
				return;
			}
			break;
		case MB_BEACON_STATE_FIXED_START:
			native_fn_02016850();
			break;
		case MB_BEACON_STATE_FIXED:
			native_fn_020168a4(ggid, tgid, attribute);
			return;
		case MB_BEACON_STATE_VOLAT_START:
			native_fn_02016a08();
			break;
		case MB_BEACON_STATE_VOLAT:
			native_fn_02016a38(ggid, tgid, attribute);
			return;
		case MB_BEACON_STATE_NEXT_GAME:
			break;
		}
	}
}
