#include "native_pxi_types.h"
s32 native_arm7_wram_037fe410(u32 tag, u32 payload, u32 error) {
    PXI_UnkStruct1 message;
    message.fields.unk_00_0 = tag;
    message.fields.unk_00_5 = error;
    message.fields.unk_00_6 = payload;
    return PXIi_SendWord(message.word);
}
