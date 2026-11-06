#include "native_main_020154c0_types.h"

int native_main_020154c0 (void)
{
	struct bitmap {
		u16 connected;
		u16 req;
		u16 kick;
		u16 boot;
		u16 mem_full;
	};
	struct bitmap bmp;
	u16 child;
	int errcode;
	MI_CpuClear16(&bmp, sizeof(struct bitmap));
	for (child = 1; child <= 15 ; child++) {
		switch (((MB_CommPWork *)native_data_main_020ec36c) ->p_comm_state[child - 1]) {
		case MB_COMM_PSTATE_CONNECTED:
			bmp.connected |= (1 << child);
			break;
		case MB_COMM_PSTATE_REQ_ACCEPTED:
			bmp.req |= (1 << child);
			break;
		case MB_COMM_PSTATE_KICKED:
			bmp.kick |= (1 << child);
			break;
		case MB_COMM_PSTATE_SEND_PROCEED:
			break;
		case MB_COMM_PSTATE_BOOT_REQUEST:
			bmp.boot |= (1 << child);
			break;
		case MB_COMM_PSTATE_MEMBER_FULL:
			bmp.mem_full |= (1 << child);
			break;
		default:
			break;
		}
	}
	if (bmp.boot) {
		errcode = native_fn_02014fa8(MB_COMM_TYPE_PARENT_BOOTREQ, bmp.boot);
	} else if (bmp.connected)   {
		errcode = native_fn_02014fa8(MB_COMM_TYPE_PARENT_SENDSTART, bmp.connected);
	} else if (bmp.mem_full)   {
		errcode = native_fn_02014fa8(MB_COMM_TYPE_PARENT_MEMBER_FULL, bmp.mem_full);
	} else if (bmp.kick)   {
		errcode = native_fn_02014fa8(MB_COMM_TYPE_PARENT_KICKREQ, bmp.kick);
	} else if (bmp.req)   {
		errcode = native_fn_02014fe8();
	} else {
		errcode = native_fn_02015224();
	}
	if ((WM_ERRCODE_MAX + 1) == errcode) {
		errcode = native_fn_02014fa8(MB_COMM_TYPE_DUMMY, 0xffff);
	}
	return errcode;
}
