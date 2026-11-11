/* State word probe and engine query.
 *
 * Returns zero unless the word at 0x02246438 + 0x18 equals 5, in which case it
 * returns the value from native_fn_02078b30. The zero is materialised before the
 * compare and returned through `popne`.
 * Unknowns: what the state word counts and what the query reads.
 */
typedef unsigned char u8;
typedef unsigned int u32;

extern u8 native_data_ov000_02246438[];
extern u32 native_fn_02078b30(void);

u32 native_ov000_022221ac(void)
{
    u32 result = 0;

    if (*(u32 *)(native_data_ov000_02246438 + 0x18) == 5)
        result = native_fn_02078b30();
    return result;
}
