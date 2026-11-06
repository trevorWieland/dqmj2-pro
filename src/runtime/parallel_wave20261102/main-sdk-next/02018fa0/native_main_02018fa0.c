#include "context_00.h"
u8 * native_main_02018fa0 (const u8 * recvbuf, MBCommChildBlockHeader * hdr, u16 child_id)
{
	u8 * ptr = (u8 *)recvbuf;
	hdr->type = *ptr++;
	switch (hdr->type) {
	case MB_COMM_TYPE_CHILD_FILEREQ:
		if (native_fn_02019148(child_id)) {
			return (u8 *)native_data_main_020ec3a4.field_0004->data_buf[child_id - 1];
		}
		hdr->req_data.piece = *ptr++;
		if (hdr->req_data.piece > native_data_main_020ec3a4.field_0008.num) {
			return ((void *)0) ;
		}
		native_fn_02008e0c(ptr, hdr->req_data.data, (u32)native_data_main_020ec3a4.field_0008.size);
		ptr = native_fn_020190bc(hdr, child_id);
		break;
	case MB_COMM_TYPE_CHILD_ACCEPT_FILEINFO:
		hdr->data.req = (u16)(0x00ff & (*ptr++));
		hdr->data.req |= (((u16)(*ptr++) << 8) & 0xff00);
		break;
	case MB_COMM_TYPE_CHILD_CONTINUE:
		hdr->data.req = (u16)(0x00ff & (*ptr++));
		hdr->data.req |= (((u16)(*ptr++) << 8) & 0xff00);
		native_fn_02008e0c(ptr, hdr->data.reserved, (u32)native_data_main_020ec3a4.field_0008.size);
		ptr += native_data_main_020ec3a4.field_0008.size;
		break;
	default:
		return ((void *)0) ;
	}
	return ptr;
}
