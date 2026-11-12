/* ov000 row 0x02220160: 280 bytes.
 *
 * What it does: 68 instructions; 11 call(s) to 0x0221d05c, 0x0221d05c, 0x0221d05c, +8 more; loops (back edge at +0x14); returns through pop {r4, r5, r6, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x110 -> constant 0x022463b0 (image word 0x022463b0)
 *   pool +0x114 -> constant 0x2aaaaaab (image word 0x2aaaaaab)
 *   back edge +0x5c -> +0x40
 *   test +0x58 cmp r4, #6
 *   test +0x60 cmp r6, #0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02220160; the literal pool and
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

extern void native_fn_0221d05c(void);
extern void native_fn_0221c8dc(void);
extern void native_fn_02228fdc(void);
extern void native_fn_0221cab0(void);
extern void native_fn_02049008(void);


asm u32 native_ov000_02220160 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #8
    mov r5, r0
    mov r6, r1
    mov r0, #16
    bl native_fn_0221d05c
    mov r1, r6
    mov r0, #17
    bl native_fn_0221d05c
    mov r1, r6
    mov r0, #18
    bl native_fn_0221d05c
    mov r1, r6
    mov r0, #19
    bl native_fn_0221d05c
    mov r4, #0
ov000_02220160_L40:
    add r0, r4, #20
    mov r0, r0, lsl #24
    mov r1, r6
    mov r0, r0, asr #24
    bl native_fn_0221d05c
    add r4, r4, #1
    cmp r4, #6
    blt ov000_02220160_L40
    cmp r6, #0
    addeq sp, sp, #8
    ldmeqia sp!, {r4, r5, r6, pc}
    ldr r4, [r5]
    mov r3, #0
    mov r1, #6
    mov r0, r5
    mov r2, r1
    str r3, [sp]
    mov r12, #1
    mov r3, #20
    str r12, [sp, #0x4]
    bl native_fn_0221c8dc
    ldr r0, =0x022463b0
    ldr r0, [r0, #0x20]
    bl native_fn_02228fdc
    ldr r1, =0x022463b0
    str r0, [r5]
    ldr r0, [r1, #0x20]
    bl native_fn_02228fdc
    ldr r2, =0x2aaaaaab
    mov r3, #6
    smull r1, r12, r2, r0
    add r12, r12, r0, lsr #31
    mul r0, r12, r3
    str r0, [r5, #0x4]
    ldr r0, =0x022463b0
    ldr r1, [r0, #0x20]
    str r1, [r0, #0x18]
    bl native_fn_0221cab0
    mov r0, r5
    ldr r1, =0x022463b0
    mov r2, #2
    str r4, [r1, #0xc]
    str r2, [sp]
    mov r1, #20
    mov r2, #0
    mov r3, #1
    bl native_fn_02049008
    mov r1, #1
    ldr r0, =0x022463b0
    strb r1, [r0]
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, pc}
}
