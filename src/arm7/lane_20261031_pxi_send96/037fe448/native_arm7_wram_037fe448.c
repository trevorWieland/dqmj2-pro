#include "native_pxi_types.h"
s32 native_arm7_wram_037fe448(u32 value)
{
    OSIntrMode irq;
    if (REG_IPC_FIFO_CNT & PXI_IPC_FIFO_CNT_ERROR) {
        REG_IPC_FIFO_CNT |= PXI_IPC_FIFO_CNT_ENABLE | PXI_IPC_FIFO_CNT_ERROR_ACK;
        return -1;
    }
    irq = OS_DisableInterrupts();
    if (REG_IPC_FIFO_CNT & PXI_IPC_FIFO_CNT_SEND_FULL) {
        OS_RestoreInterrupts(irq);
        return -2;
    } else {
        REG_IPC_FIFO_SEND = value;
        OS_RestoreInterrupts(irq);
        return 0;
    }
}
