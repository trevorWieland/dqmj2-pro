/* ov000 row 0x021e182c: 104 bytes.
 *
 * What it does: 25 instructions; 3 call(s) to 0x021e1878, 0x0205d750, 0x021e184c; loops (back edge at +0x2c); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x64 -> constant 0x022322d0 (image word 0x022322d0)
 *   branch +0x28 -> +0x4c
 *   back edge +0x58 -> +0x20
 *   test +0x24 cmp r0, #0
 *   test +0x34 cmp r0, #0
 *   test +0x40 cmp r0, #0
 *   test +0x50 cmp r4, #4
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e182c; the literal pool and
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

extern void native_fn_0205d750(void);


asm u32 native_ov000_021e182c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    mov r5, #0
    mov r10, #1
    ldr r6, =0x022322d0
    mov r4, r5
    mov r9, r5
    mvn r8, #0
    mov r7, r10
ov000_021e182c_L20:
    ldrsb r0, [r6]
    cmp r0, #0
    blt ov000_021e182c_L4c
    bl native_fn_0205d750
    ldrb r0, [r0]
    cmp r0, #0
    moveq r0, r10
    movne r0, r9
    cmp r0, #0
    movne r5, r7
    strneb r8, [r6]
ov000_021e182c_L4c:
    add r4, r4, #1
    cmp r4, #4
    add r6, r6, #1
    blt ov000_021e182c_L20
    mov r0, r5
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
