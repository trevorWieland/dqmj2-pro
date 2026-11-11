/* Reset five state bytes after a mode call.
 *
 * Calls native_fn_0206cc70 with mode 2, then fills the five bytes at 0x02246340
 * with 0xff. The fill is set up only after the call (the image loads the table
 * literal following the `bl`), and the value is materialised with `mvn r0, #0`,
 * so the cursor is a signed-byte pointer and the value is -1.
 * Unknowns: what the mode call selects and what the five bytes gate.
 */
typedef signed char s8;
typedef unsigned char u8;
typedef int s32;
typedef unsigned int u32;

extern s8 native_data_ov000_02246340[];
extern void native_fn_0206cc70(u32);

void native_ov000_0221d8e0(void)
{
    native_fn_0206cc70(2);

    {
        s8 *cursor = native_data_ov000_02246340;
        s32 index = 0;

        do {
            index++;
            *cursor++ = -1;
        } while (index < 5);
    }
}
