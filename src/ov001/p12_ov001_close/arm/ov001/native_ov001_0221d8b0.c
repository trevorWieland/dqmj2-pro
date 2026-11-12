/* ov001 row 0x0221d8b0: 192 bytes.
 *
 * What it does: 48 instructions; 6 call(s) to 0x021db8d0, 0x021db8d0, 0x021f07dc, +3 more; loops (back edge at +0x30); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: block fill (48 instructions, 6 calls, 2 branches, 6 back edges, 0 literal slots).
 *
 *   branch +0x38 -> +0x94
 *   branch +0x48 -> +0x94
 *   back edge +0xa0 -> +0x2c
 *   back edge +0xb0 -> +0x24
 *   test +0x34 cmp r0, #0
 *   test +0x44 cmp r0, #0
 *   test +0x58 cmp r0, #0
 *   test +0x84 cmp r8, r0
 *   test +0x98 cmp r7, #3
 *   test +0xa8 cmp r11, #3
 *   1 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221d8b0; the literal pool and
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
extern void native_fn_021f07dc(void);
extern void native_fn_021dbd24(void);


asm u32 native_ov001_0221d8b0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    ldr r1, [r0, #0x8]
    mov r11, #0
    ldr r9, [r0, #0x4]
    str r1, [sp, #0xc]
    mov r6, #1
    mov r5, r11
    mov r4, #2
ov001_0221d8b0_L24:
    ldr r10, [sp, #0xc]
    mov r7, #0
ov001_0221d8b0_L2c:
    mov r0, r9
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221d8b0_L94
    mov r0, r10
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221d8b0_L94
    ldrb r0, [r10, #0x356]
    mov r1, r9
    mov r2, r5
    cmp r0, #0
    streqb r6, [r10, #0x356]
    str r5, [sp]
    stmib sp, {r4, r5}
    mov r0, r10
    mov r3, r5
    bl native_fn_021f07dc
    ldrb r1, [r10, #0x356]
    mul r8, r1, r0
    mov r0, r9
    bl native_fn_021dbd24
    cmp r8, r0
    addge sp, sp, #16
    movge r0, #1
    ldmgeia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_0221d8b0_L94:
    add r7, r7, #1
    cmp r7, #3
    add r10, r10, #1088
    blt ov001_0221d8b0_L2c
    add r11, r11, #1
    cmp r11, #3
    add r9, r9, #1088
    blt ov001_0221d8b0_L24
    mov r0, #0
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
