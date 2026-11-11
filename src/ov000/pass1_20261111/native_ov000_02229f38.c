/* Signed halfword from a stride-6 record.
 *
 * Reads the signed halfword at `0x0222e000 + index * 6 + offset * 2`, i.e.
 * field `offset` of a three-halfword record. The image computes `offset * 2`
 * with a separate `lsl` and then loads through the pair, so the address is
 * written as flat byte arithmetic rather than as a typed array index.
 * Unknowns: record semantics; the table's extent.
 */
typedef short s16;
typedef int s32;

extern unsigned char native_data_ov000_0222e000[];

s16 native_ov000_02229f38(s32 index, s32 offset)
{
    return *(s16 *)(native_data_ov000_0222e000 + index * 6 + offset * 2);
}
