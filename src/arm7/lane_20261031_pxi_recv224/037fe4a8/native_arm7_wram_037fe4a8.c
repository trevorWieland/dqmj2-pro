#include "native_pxi_types.h"
void native_arm7_wram_037fe4a8(void) {
    PXI_UnkStruct1 fifoSend;
    void (*callback)(u32, u32, u32);
    s32 result;
    u32 temp_r0;
    OSIntrMode irq;

    while (true) {
        if (REG_IPC_FIFO_CNT & PXI_IPC_FIFO_CNT_ERROR) {
            REG_IPC_FIFO_CNT |= PXI_IPC_FIFO_CNT_ENABLE | PXI_IPC_FIFO_CNT_ERROR_ACK;
            result = -3;
        } else {
            irq = OS_DisableInterrupts();
            if (REG_IPC_FIFO_CNT & PXI_IPC_FIFO_CNT_RECV_EMPTY) {
                OS_RestoreInterrupts(irq);
                result = -4;
            } else {
                fifoSend = REG_04100000;
                OS_RestoreInterrupts(irq);
                result = 0;
            }
        }
        if (result == -4) {
            break;
        }
        if (result != -3) {
            temp_r0 = fifoSend.fields.unk_00_0;
            if (temp_r0 != 0) {
                callback = sFifoRecvCallbacks[temp_r0];
                if (callback != NULL) {
                    callback(temp_r0, fifoSend.fields.unk_00_6, fifoSend.fields.unk_00_5);
                } else if (fifoSend.fields.unk_00_5 == 0) {
                    fifoSend.fields.unk_00_5 = 1;
                    (void)PXIi_SendWord(fifoSend.word);
                }
            }
        }
    }
}
