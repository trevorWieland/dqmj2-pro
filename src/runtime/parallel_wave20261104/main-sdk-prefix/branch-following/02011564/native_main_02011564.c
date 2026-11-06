#include "context_00.h"
void native_main_02011564 (u32 data, u32 wait)
{
	while (native_fn_0200a440(PXI_FIFO_TAG_CARD, data, 0 ) != PXI_FIFO_SUCCESS) {
		native_fn_020004fc((s32)wait);
	}
}
