/* ov001 row 0x021e82fc: 156 bytes.
 *
 * What it does: 33 instructions; 2 call(s) to 0x0207afec, 0x0207afec; loops (back edge at +0x1c); returns through pop {r4, pc}; 6 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (33 instructions, 2 calls, 1 branch, 2 back edges, 6 literal slots).
 *
 *   pool +0x84 -> constant 0x02238d1c (image word 0x02238d1c)
 *   pool +0x88 -> constant 0x02238d1e (image word 0x02238d1e)
 *   pool +0x8c -> constant 0x02238d1f (image word 0x02238d1f)
 *   pool +0x90 -> constant 0x02238d2e (image word 0x02238d2e)
 *   pool +0x94 -> constant 0x02238d30 (image word 0x02238d30)
 *   pool +0x98 -> constant 0x02238d31 (image word 0x02238d31)
 *   branch +0x10 -> +0x4c
 *   test +0x04 cmp r1, #0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e82fc; the literal pool and
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

extern void native_fn_0207afec(void);


asm u32 native_ov001_021e82fc (register u32 a0)
{
    stmdb sp!, {r4, lr}
    cmp r1, #0
    mov r1, #6
    mul r4, r2, r1
    bne ov001_021e82fc_L4c
    ldr r1, =0x02238d1c
    strh r0, [r1, r4]
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    ldr r1, =0x02238d1e
    mov r0, r0, lsl #24
    movs r0, r0, lsr #28
    moveq r2, #0
    movne r2, #1
    strb r2, [r1, r4]
    ldr r0, =0x02238d1f
    mov r1, #0
    strb r1, [r0, r4]
    ldmia sp!, {r4, pc}
ov001_021e82fc_L4c:
    ldr r1, =0x02238d2e
    strh r0, [r1, r4]
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    ldr r1, =0x02238d30
    mov r0, r0, lsl #24
    movs r0, r0, lsr #28
    moveq r2, #1
    ldr r0, =0x02238d31
    movne r2, #0
    strb r2, [r1, r4]
    mov r1, #0
    strb r1, [r0, r4]
    ldmia sp!, {r4, pc}
}
