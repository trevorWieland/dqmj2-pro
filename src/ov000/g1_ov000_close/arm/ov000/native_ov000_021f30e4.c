/* ov000 row 0x021f30e4: 176 bytes.
 *
 * What it does: 44 instructions; 4 call(s) to 0x02049ad0, 0x02049ffc, 0x0204a574, +1 more; loops (back edge at +0x40); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, pc}
 *
 * Decoded shape: block fill.
 *
 *   branch +0x4c -> +0x94
 *   branch +0x6c -> +0x94
 *   back edge +0xa4 -> +0x30
 *   test +0x18 cmp r0, #0
 *   test +0x48 cmp r0, #0
 *   test +0x68 cmp r12, r0
 *   test +0xa0 cmp r6, r0
 *   1 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f30e4; the literal pool and
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

extern void native_fn_02049ad0(void);
extern void native_fn_02049ffc(void);
extern void native_fn_0204a574(void);


asm u32 native_ov000_021f30e4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #12
    mov r10, r0
    ldrh r0, [r10, #12]
    mov r9, r1
    mov r8, r2
    cmp r0, #0
    mov r6, #0
    addle sp, sp, #12
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
    mov r5, #1
    mov r4, r6
ov000_021f30e4_L30:
    add r0, r6, #3
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    mov r0, r7
    bl native_fn_02049ad0
    ldr r0, [r0]
    cmp r0, #0
    beq ov000_021f30e4_L94
    ldr r0, [r0, #0x4]
    bl native_fn_02049ffc
    ldr r1, [r10, #0x4]
    ldrh r0, [r10, #14]
    add r1, r1, r6
    and r12, r1, #255
    cmp r12, r0
    bge ov000_021f30e4_L94
    add r3, r9, r12, lsl #2
    ldrh r2, [r3, #2]
    mov r0, r7
    mov r1, r8
    stmia sp, {r2, r5}
    str r4, [sp, #0x8]
    ldrb r2, [r9, r12, lsl #2]
    ldrb r3, [r3, #0x1]
    bl native_fn_0204a574
ov000_021f30e4_L94:
    ldrh r0, [r10, #12]
    add r1, r6, #1
    and r6, r1, #255
    cmp r6, r0
    blt ov000_021f30e4_L30
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
}
