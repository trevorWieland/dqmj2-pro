/* Clear five state bytes and install the default option.
 *
 * Fills the five bytes at 0x02246340 with 0xff, then tail-calls
 * native_fn_02008d78 with the table at 0x02246348, zero and 88. The image
 * materialises the fill value with `mvn r0, #0`, so the cursor is a signed-byte
 * pointer and the value is -1, not 255.
 * Unknowns: what the five bytes and the callee's option table mean.
 */
typedef signed char s8;
typedef unsigned char u8;
typedef int s32;
typedef unsigned int u32;

extern s8 native_data_ov000_02246340[];
extern u8 native_data_ov000_02246348;
extern u32 native_fn_02008d78(u32, u32, u32);

u32 native_ov000_0221d438(void)
{
    s8 *cursor = native_data_ov000_02246340;
    s32 index = 0;

    do {
        index++;
        *cursor++ = -1;
    } while (index < 5);
    return native_fn_02008d78((u32)&native_data_ov000_02246348, 0, 88);
}
