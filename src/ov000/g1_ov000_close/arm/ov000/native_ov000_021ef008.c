/* ov000 row 0x021ef008: 168 bytes.
 *
 * What it does: 40 instructions; 5 call(s) to 0x02049ad0, 0x0204b53c, 0x0205f9e4, +2 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xa0 -> constant 0x02236bd0 (image word 0x02236bd0)
 *   pool +0xa4 -> constant 0x02236bec (image word 0x02236bec)
 *   branch +0x2c -> +0x64
 *   back edge +0x94 -> +0x7c
 *   test +0x28 cmp r1, #0
 *   test +0x90 cmp r6, #6
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021ef008; the literal pool and
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
extern void native_fn_0204b53c(void);
extern void native_fn_0205f9e4(void);
extern void native_fn_02048a44(void);


asm u32 native_ov000_021ef008 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #4
    ldr r2, [r0]
    ldr r0, [r0, #0x4]
    sub r0, r2, r0
    add r0, r1, r0
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    ldr r1, [r0]
    cmp r1, #0
    beq ov000_021ef008_L64
    ldr r1, [r1, #0x4]
    ldr r2, =0x02236bd0
    ldrb r3, [r1, #0x1c]
    add r1, sp, #0
    mov r3, r3, lsl #3
    strh r3, [sp]
    ldr r3, [r0]
    ldr r0, [r2, #0x14]
    ldr r2, [r3, #0x4]
    ldrb r2, [r2, #0x1d]
    mov r2, r2, lsl #3
    strh r2, [sp, #2]
    bl native_fn_0204b53c
ov000_021ef008_L64:
    ldr r0, =0x02236bd0
    ldr r0, [r0, #0x14]
    bl native_fn_0205f9e4
    ldr r5, =0x02236bec
    mov r6, #0
    mov r4, #1
ov000_021ef008_L7c:
    ldr r0, [r5, r6, lsl #2]
    mov r1, r4
    add r0, r0, #8
    bl native_fn_02048a44
    add r6, r6, #1
    cmp r6, #6
    blt ov000_021ef008_L7c
    add sp, sp, #4
    ldmia sp!, {r3, r4, r5, r6, pc}
}
