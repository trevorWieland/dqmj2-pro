/* Address selector over three consecutive flag bytes.
 *
 * Mode 2 and mode 4 pick the first and second byte; mode 6 and every other mode
 * share the third, which is why the image compares 6 and then falls into the
 * same body as the default.
 * Unknowns: what the three flags mean; the switch is over an opaque mode word.
 */
typedef unsigned char u8;
typedef signed int s32;

extern u8 native_data_ov000_02236d94;
extern u8 native_data_ov000_02236d95;
extern u8 native_data_ov000_02236d96;

u8 *native_ov000_021f2764(s32 mode)
{
    switch (mode) {
    case 2:
        return &native_data_ov000_02236d94;
    case 4:
        return &native_data_ov000_02236d95;
    case 6:
    default:
        return &native_data_ov000_02236d96;
    }
}
