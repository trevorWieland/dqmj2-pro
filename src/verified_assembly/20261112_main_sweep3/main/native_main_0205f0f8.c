/* main row 0x0205f0f8: 68 bytes.
 *
 * What it does: Scans 16 records of 8 bytes from the pooled base: returns the index of the first record whose byte at +7 has bit 0 clear and whose halfword at +4 is negative, else -1.
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x40 -> constant 0x021b8b10 (image word 0x021b8b10)
 *   branch +0x18 -> +0x2c
 *   back edge +0x38 -> +0x0c
 *   test +0x20 cmp r1, #0
 *   test +0x30 cmp r2, #0x10
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0205f0f8; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the table, the record layout and the callee contract are not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;



asm u32 native_main_0205f0f8 (register u32 a0)
{
    ldr r3, =0x021b8b10
    mvn r0, #0
    mov r2, #0
main_0205f0f8_Lc:
    ldrb r1, [r3, #7]
    mov r1, r1, lsl #0x1f
    movs r1, r1, lsr #0x1f
    bne main_0205f0f8_L2c
    ldrsh r1, [r3, #4]
    cmp r1, #0
    movlt r0, r2
    bxlt lr
main_0205f0f8_L2c:
    add r2, r2, #1
    cmp r2, #0x10
    add r3, r3, #8
    blt main_0205f0f8_Lc
    bx lr
}
