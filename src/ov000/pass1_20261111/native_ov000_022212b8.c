/* Current selection to halfword and byte pair.
 *
 * Reads the selected index from byte 3 of the byte at 0x022463b0 and writes the
 * index's signed halfword from the table at 0x022463dc and its byte from the
 * table at 0x02246424 through the two out pointers. This is the no-argument
 * sibling of 0x0222131c: same two tables, index taken from the state byte.
 * Unknowns: what the state byte tracks and who sets it.
 */
typedef signed char s8;
typedef short s16;
typedef unsigned char u8;
typedef unsigned short u16;

extern u8 native_data_ov000_022463b0[];
extern s16 native_data_ov000_022463dc[];
extern u8 native_data_ov000_02246424[];

void native_ov000_022212b8(u16 *out16, u8 *out8)
{
    u8 index = native_data_ov000_022463b0[3];

    *out16 = *(s16 *)((u8 *)native_data_ov000_022463dc + index * 2);
    *out8 = native_data_ov000_02246424[index];
}
