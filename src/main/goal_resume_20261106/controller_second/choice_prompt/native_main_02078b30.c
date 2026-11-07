#include "choice_prompt.h"

u32 native_main_02078b30(void)
{
    TextFont *font = &native_data_021c9698;
    TextBindingSlot *slot = native_fn_02049ae4();
    u16 *output = native_fn_02049f24();
    u32 alternate = native_fn_0206c100();
    s32 choice = native_fn_0206c120();
    const u8 *text = 0;
    u32 message = 0;
    native_fn_02049f30();
    switch (choice) {
    case 0:
        text = native_fn_0205dc70(5, 2, 60);
        message = 57;
        break;
    case 1:
        text = native_fn_0205dc70(5, 2, 61);
        message = 58;
        break;
    case 2:
        text = native_fn_0205dc70(5, 2, 62);
        message = 59;
        break;
    case -1:
        if (alternate == 0) {
            text = native_fn_0205dc70(5, 2, 63);
            message = 60;
        } else {
            text = native_fn_0205dc70(5, 2, 64);
            message = 61;
        }
        break;
    }
    if (text != 0) {
        native_fn_02046af4(font, text, 28, 0, output, 255);
        native_fn_02049f14(output);
    }
    native_fn_ov000_02217bdc(5, 7, message, 1, 1, 87);
    if (slot->stream != 0) {
        native_fn_020853c8(slot->binding, slot->stream);
    }
    native_fn_02068f60(0);
    native_fn_0206b35c();
    return 0;
}
