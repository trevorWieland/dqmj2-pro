/* ov001 row 0x0221e9c8: 100 bytes.
 *
 * What it does: 25 instructions; 4 call(s) to 0x021db8d0, 0x021dbe5c, 0x0221e9d8, +1 more; loops (back edge at +0x14); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 4 calls (25 instructions, 4 calls, 2 branches, 4 back edges, 0 literal slots).
 *
 *   branch +0x1c -> +0x30
 *   branch +0x2c -> +0x4c
 *   back edge +0x48 -> +0x10
 *   test +0x18 cmp r0, #0
 *   test +0x28 cmp r0, #1
 *   test +0x30 cmp r4, #2
 *   test +0x40 cmp r4, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221e9c8; the literal pool and
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
extern void native_fn_021dbe5c(void);
extern void native_fn_0221873c(void);


asm u32 native_ov001_0221e9c8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r0
    ldr r5, [r6, #0x8]
    mov r4, #0
ov001_0221e9c8_L10:
    mov r0, r5
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221e9c8_L30
    mov r0, r5
    bl native_fn_021dbe5c
    cmp r0, #1
    bgt ov001_0221e9c8_L4c
ov001_0221e9c8_L30:
    cmp r4, #2
    moveq r0, #1
    ldmeqia sp!, {r4, r5, r6, pc}
    add r4, r4, #1
    cmp r4, #3
    add r5, r5, #1088
    blt ov001_0221e9c8_L10
ov001_0221e9c8_L4c:
    mov r1, #3
    ldr r0, [r6, #0x8]
    sub r2, r1, #5
    mov r3, #2
    bl native_fn_0221873c
    ldmia sp!, {r4, r5, r6, pc}
}
