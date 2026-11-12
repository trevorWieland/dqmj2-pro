/* ov001 row 0x02219e28: 76 bytes.
 *
 * What it does: 19 instructions; 2 call(s) to 0x021db8d0, 0x02219e38; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: block load (19 instructions, 2 calls, 0 branches, 2 back edges, 0 literal slots).
 *
 *   back edge +0x38 -> +0x10
 *   test +0x18 cmp r0, #0
 *   test +0x2c cmpne r1, r0
 *   test +0x34 cmp r5, #3
 *   test +0x3c cmp r6, #1
 *   1 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02219e28; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021db8d0(void);


asm u32 native_ov001_02219e28 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r6, #0
    ldmia r0, {r4, r7}
    mov r5, r6
ov001_02219e28_L10:
    mov r0, r7
    bl native_fn_021db8d0
    cmp r0, #0
    ldrneb r0, [r7, #0x31f]
    ldrneb r1, [r4, #0x31f]
    add r5, r5, #1
    add r7, r7, #1088
    cmpne r1, r0
    addne r6, r6, #1
    cmp r5, #3
    blt ov001_02219e28_L10
    cmp r6, #1
    moveq r0, #1
    movne r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
