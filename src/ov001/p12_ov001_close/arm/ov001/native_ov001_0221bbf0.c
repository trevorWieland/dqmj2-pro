/* ov001 row 0x0221bbf0: 172 bytes.
 *
 * What it does: 43 instructions; 6 call(s) to 0x021db8d0, 0x021e2b1c, 0x021e81d0, +3 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 6 calls (43 instructions, 6 calls, 5 branches, 6 back edges, 0 literal slots).
 *
 *   branch +0x10 -> +0xa4
 *   branch +0x24 -> +0x94
 *   branch +0x38 -> +0x94
 *   branch +0x48 -> +0x94
 *   branch +0x80 -> +0x94
 *   back edge +0xa0 -> +0x18
 *   test +0x0c cmp r1, #0
 *   test +0x20 cmp r0, #0
 *   test +0x34 cmp r0, #0
 *   test +0x44 cmp r0, #1
 *   test +0x7c cmp r0, #4
 *   test +0x88 cmp r0, #2
 *   test +0x98 cmp r4, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221bbf0; the literal pool and
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
extern void native_fn_021e2b1c(void);
extern void native_fn_021e81d0(void);
extern void native_fn_0207afec(void);


asm u32 native_ov001_0221bbf0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r1, [r0, #0x14]
    ldr r5, [r0, #0x8]
    cmp r1, #0
    beq ov001_0221bbf0_La4
    mov r4, #0
ov001_0221bbf0_L18:
    mov r0, r5
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221bbf0_L94
    ldrb r0, [r5, #0x31e]
    ldrb r1, [r5, #0x31f]
    bl native_fn_021e2b1c
    cmp r0, #0
    bne ov001_0221bbf0_L94
    ldr r0, [r5, #0x1e8]
    ldrb r0, [r0, #0x97]
    cmp r0, #1
    bhi ov001_0221bbf0_L94
    ldrb r0, [r5, #0x31e]
    ldrb r1, [r5, #0x31f]
    bl native_fn_021e81d0
    ldrh r6, [r0]
    mov r0, r6
    bl native_fn_0207afec
    ldrb r7, [r0, #0x21]
    mov r0, r6
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #20
    mov r0, r0, lsr #28
    cmp r0, #4
    bne ov001_0221bbf0_L94
    sub r0, r7, #16
    cmp r0, #2
    movls r0, #1
    ldmlsia sp!, {r3, r4, r5, r6, r7, pc}
ov001_0221bbf0_L94:
    add r4, r4, #1
    cmp r4, #3
    add r5, r5, #1088
    blt ov001_0221bbf0_L18
ov001_0221bbf0_La4:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
