#include "context.h"

/* Shared ov006 display state at 0x0221C0D8: a 16-bit scale at +0x02 and a
   pointer at +0x04 to the current record. The record's level byte is at +0x51,
   its derived height halfword at +0x40 and its palette selector byte at +0x53. */
struct native_state_021f8050 {
    u16 field_00;
    u16 field_02;
    u8 *field_04;
};

extern struct native_state_021f8050 native_data_ov006_0221c0d8;

/* Scale one mode value; ARM code in main, so this is a BLX from Thumb. */
extern s32 native_fn_02002480(s32 value, s32 scale);
extern void native_ov006_021fe60c(s32 selector, s32 first, s32 second, s32 third,
                                   u32 value);

/* ov006 row 0x021F8050: 116 bytes. Derive the current record's height from its
   +0x51 level, pick one of three palette selectors with a matching +0x53 byte,
   scale the display's +0x02 factor by that selector through ARM code once the
   selector is non-zero, and hand selector 0x55/0xEC/0x3F plus the scaled value
   to the Thumb blit entry. The call at +0x5A targets ARM code and is a BLX
   immediate in the image. Unknown: what the three selectors 0/0x1F/0x37 mean
   and what 0x021FE60C does with them. */
void native_ov006_021f8050(void)
{
    u32 value = 0;
    u32 selector;

    *(u16 *)(native_data_ov006_0221c0d8.field_04 + 0x40) =
        (u16)((native_data_ov006_0221c0d8.field_04[0x51] - 4) * 0x1C);

    if (native_data_ov006_0221c0d8.field_04[0x51] <= 4) {
        selector = 0;
        native_data_ov006_0221c0d8.field_04[0x53] = 0;
    } else if (native_data_ov006_0221c0d8.field_04[0x51] <= 8) {
        selector = 1;
        native_data_ov006_0221c0d8.field_04[0x53] = 0x1F;
    } else {
        selector = 2;
        native_data_ov006_0221c0d8.field_04[0x53] = 0x37;
    }

    if (selector != 0)
        value = native_fn_02002480(native_data_ov006_0221c0d8.field_02
                                   * native_data_ov006_0221c0d8.field_04[0x53],
                                   *(u16 *)(native_data_ov006_0221c0d8.field_04 + 0x40));

    native_ov006_021fe60c(selector, 0x55, 0xEC, 0x3F, value);
}

