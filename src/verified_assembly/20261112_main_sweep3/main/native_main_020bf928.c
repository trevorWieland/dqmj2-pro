/* main row 0x020bf928: 56 bytes.
 *
 * What it does: Linear search of a 100-entry, 8-byte-record table (base from the pooled pointer's +8 word) for the record whose first word equals r0; returns its byte at +7, or -1.
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x34 -> constant 0x021d4bec (image word 0x021d4bec)
 *   back edge +0x28 -> +0x0c
 *   test +0x10 cmp r0, r1
 *   test +0x24 cmp r2, #0x64
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020bf928; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the field meanings and the callee contracts are not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;



asm u32 native_main_020bf928 (register u32 a0)
{
    ldr r1, =0x021d4bec
    mov r2, #0
    ldr r3, [r1, #8]
main_020bf928_Lc:
    ldr r1, [r3, r2, lsl #3]
    cmp r0, r1
    addeq r0, r3, r2, lsl #3
    ldreqsb r0, [r0, #7]
    bxeq lr
    add r2, r2, #1
    cmp r2, #0x64
    blt main_020bf928_Lc
    mvn r0, #0
    bx lr
}
