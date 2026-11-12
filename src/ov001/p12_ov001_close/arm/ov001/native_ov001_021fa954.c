/* ov001 row 0x021fa954: 128 bytes.
 *
 * What it does: 31 instructions; 5 call(s) to 0x021d9494, 0x021d9494, 0x021da480, +2 more; loops (back edge at +0x14); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 5 calls (31 instructions, 5 calls, 0 branches, 5 back edges, 1 literal slot).
 *
 *   pool +0x7c -> constant 0x02239a14 (image word 0x02239a14)
 *   test +0x5c cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fa954; the literal pool and
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

extern void native_fn_021d9494(void);
extern void native_fn_021da480(void);
extern void native_fn_021fa8ac(void);


asm u32 native_ov001_021fa954 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x02239a14
    mov r1, #0
    ldr r0, [r0, #0x34]
    mov r2, r1
    bl native_fn_021d9494
    ldr r0, =0x02239a14
    mov r1, #0
    ldr r0, [r0, #0x40]
    mov r2, r1
    bl native_fn_021d9494
    ldr r0, =0x02239a14
    mov r1, #1
    ldr r0, [r0, #0x34]
    bl native_fn_021da480
    ldr r0, =0x02239a14
    mov r1, #1
    ldr r0, [r0, #0x40]
    bl native_fn_021da480
    ldr r1, =0x02239a14
    ldr r0, [r1, #0x34]
    ldr r1, [r1, #0x40]
    bl native_fn_021fa8ac
    cmp r0, #0
    ldrne r0, =0x02239a14
    movne r1, #8
    ldreq r0, =0x02239a14
    moveq r1, #10
    strb r1, [r0, #0xa]
    mov r0, #1
    ldmia sp!, {r3, pc}
}
