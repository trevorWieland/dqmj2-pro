/* ov001 row 0x0221a94c: 108 bytes.
 *
 * What it does: 26 instructions; 5 call(s) to 0x021db8d0, 0x021dbe68, 0x0221a99c, +2 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 5 calls (26 instructions, 5 calls, 1 branch, 4 back edges, 1 literal slot).
 *
 *   pool +0x68 -> constant 0x000005dc (image word 0x000005dc)
 *   branch +0x20 -> +0x34
 *   branch +0x30 -> +0x50
 *   back edge +0x4c -> +0x14
 *   test +0x1c cmp r0, #0
 *   test +0x2c cmp r0, r4
 *   test +0x34 cmp r6, #2
 *   test +0x44 cmp r6, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221a94c; the literal pool and
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
extern void native_fn_021dbe68(void);
extern void native_fn_0221873c(void);


asm u32 native_ov001_0221a94c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r5, [r0, #0x4]
    ldr r4, =0x000005dc
    mov r6, #0
    mov r7, r5
ov001_0221a94c_L14:
    mov r0, r7
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221a94c_L34
    mov r0, r7
    bl native_fn_021dbe68
    cmp r0, r4
    blt ov001_0221a94c_L50
ov001_0221a94c_L34:
    cmp r6, #2
    moveq r0, #1
    ldmeqia sp!, {r3, r4, r5, r6, r7, pc}
    add r6, r6, #1
    cmp r6, #3
    add r7, r7, #1088
    blt ov001_0221a94c_L14
ov001_0221a94c_L50:
    mov r0, r5
    mov r1, #4
    mov r2, #2
    mov r3, #0
    bl native_fn_0221873c
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
