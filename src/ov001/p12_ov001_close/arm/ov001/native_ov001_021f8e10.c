/* ov001 row 0x021f8e10: 96 bytes.
 *
 * What it does: 23 instructions; 3 call(s) to 0x021db438, 0x021db8d0, 0x021f8e34; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 3 calls (23 instructions, 3 calls, 0 branches, 3 back edges, 1 literal slot).
 *
 *   pool +0x5c -> constant 0x0223989c (image word 0x0223989c)
 *   back edge +0x54 -> +0x24
 *   test +0x18 cmp r0, #0
 *   test +0x38 cmp r0, #0
 *   test +0x48 cmpne r0, #0
 *   test +0x50 cmp r6, #3
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f8e10; the literal pool and
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

extern void native_fn_021db438(void);
extern void native_fn_021db8d0(void);


asm u32 native_ov001_021f8e10 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r0, =0x0223989c
    mov r6, #0
    ldr r0, [r0, #0x84]
    mov r4, #1
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    moveq r7, #1
    movne r7, #0
ov001_021f8e10_L24:
    mov r0, r7
    mov r1, r6
    bl native_fn_021db438
    mov r5, r0
    bl native_fn_021db8d0
    cmp r0, #0
    addne r0, r5, #512
    ldrnesb r0, [r0, #103]
    add r6, r6, #1
    cmpne r0, #0
    strneb r4, [r5, #0x431]
    cmp r6, #3
    blt ov001_021f8e10_L24
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
