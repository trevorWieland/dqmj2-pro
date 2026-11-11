/* Single-bit flag writer.
 *
 * Assigns bit 1 of the byte flag at 0x022381b4 from the low bit of `value`.
 * The image masks the argument with `and #255` before the `lsl #31` / `bic #2` /
 * `orr ..., lsr #30` one-bit field store, so the argument is a 32-bit value
 * truncated to a byte at the store, not a u8 parameter.
 * Unknowns: the flag's meaning and the other seven bits' owners.
 */
typedef unsigned char u8;
typedef unsigned int u32;

typedef struct {
    u8 bit0 : 1;
    u8 bit1 : 1;
    u8 rest : 6;
} FlagBits;

extern volatile FlagBits native_data_ov000_022381b4;

void native_ov000_02206158(u32 value)
{
    native_data_ov000_022381b4.bit1 = (u8)value;
}
