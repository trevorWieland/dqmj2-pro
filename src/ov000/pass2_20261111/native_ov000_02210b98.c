/* Store the fixed-point square of the value into the record's 0x2b8 word.
 *
 * Only an active record (state byte 0x274 set) is written. The image squares the
 * argument as a signed 64-bit product, rounds by 0x800 and keeps the high 32
 * bits of the >>12 result; the argument is returned unchanged either way.
 * Unknowns: the fixed-point unit and what the stored value drives.
 */
typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
typedef signed long long s64;

#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))

extern u8 native_data_ov000_02238634[];

s32 native_ov000_02210b98(s32 index, s32 value)
{
    u8 *record = native_data_ov000_02238634 + index * 0x2c4;

    if (M2C_FIELD(record, u8 *, 0x274) != 0) {
        s64 scaled = ((s64)value * value + 0x800) >> 12;

        M2C_FIELD(record, s32 *, 0x2b8) = (s32)scaled;
    }
    return value;
}
