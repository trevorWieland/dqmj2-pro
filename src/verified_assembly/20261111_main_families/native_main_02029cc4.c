/* Replace a five-bit field and mirror the word to hardware (0x02029cc4, 52 bytes).
 *
 * Reads the word at 0x020edd0c + 0x14, saves bits 16-23, replaces bits 16-20
 * with the caller's value, writes the word back and mirrors it to 0x04000350;
 * returns the saved bits masked to a byte.
 *
 * Unknowns: which hardware register 0x04000350 is and what the five-bit field selects.
 *
 * Body: the measured instruction stream. C forms and every installed mwccarm
 * build/profile were measured against this row first; the C form is 48 bytes: mwcc schedules the two pool loads after the read and
 * the mirror store differently, and reorders the mask and insert.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;
extern u8 native_data_020edd0c[];
extern u8 native_data_04000350[];


asm u32 native_main_02029cc4 (register u32 value)
{
    ldr r1, =native_data_020edd0c
    ldr r2, =native_data_04000350
    ldr r3, [r1, #0x14]
    and r12, r3, #0x1f0000
    bic r3, r3, #0x1f0000
    orr r3, r3, r0, lsl #16
    mov r12, r12, lsr #16
    str r3, [r1, #0x14]
    and r0, r12, #0xff
    str r3, [r2]
    bx lr
}
