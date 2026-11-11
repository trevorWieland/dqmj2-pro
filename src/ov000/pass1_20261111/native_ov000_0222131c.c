/* Record index to halfword and byte pair.
 *
 * Writes the signed halfword `index` of the table at 0x022463dc through `out16`
 * and the byte `index` of the table at 0x02246424 through `out8`. Both tables
 * are indexed by byte arithmetic (`lsl #1` then the load), not by a typed array
 * subscript, which is what the image shows.
 * Unknowns: what the two parallel tables describe.
 */
typedef signed char s8;
typedef short s16;
typedef int s32;
typedef unsigned char u8;
typedef unsigned short u16;

extern s16 native_data_ov000_022463dc[];
extern u8 native_data_ov000_02246424[];

void native_ov000_0222131c(s32 index, u16 *out16, u8 *out8)
{
    *out16 = *(s16 *)((u8 *)native_data_ov000_022463dc + index * 2);
    *out8 = native_data_ov000_02246424[index];
}
