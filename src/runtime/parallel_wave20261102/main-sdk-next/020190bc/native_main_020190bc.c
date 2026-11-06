#include "context_00.h"
u8 * native_main_020190bc (const MBCommChildBlockHeader * hdr, u16 child)
{
	u8 piece;
	u8 * ptr;
	if (native_data_main_020ec3a4.field_0004 == ((void *)0) ) {
		return ((void *)0) ;
	}
	piece = hdr->req_data.piece;
	if (piece > native_data_main_020ec3a4.field_0008.num) {
		return ((void *)0) ;
	}
	ptr = ((u8 *)native_data_main_020ec3a4.field_0004->data_buf[child - 1]) + (piece * native_data_main_020ec3a4.field_0008.size);
	native_fn_02008e0c(&hdr->req_data.data[0], ptr, (u32)native_data_main_020ec3a4.field_0008.size);
	native_data_main_020ec3a4.field_0004->data_bmp[child - 1] |= (1 << piece);
	((void)0) ;
	if (native_fn_02019148(child)) {
		return (u8 *)native_data_main_020ec3a4.field_0004->data_buf[child - 1];
	}
	return ((void *)0) ;
}
