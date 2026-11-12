/* ov000 row 0x021f1968: 124 bytes.
 *
 * What it does: 31 instructions; 2 call(s) to 0x021f3544, 0x021f3544; no back edge; returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   test +0x44 cmp r4, r2, lsr #17
 *   test +0x54 cmp r4, r2, lsr #17
 *   test +0x60 cmp r1, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f1968; the literal pool and
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

extern void native_fn_021f3544(void);


asm u32 native_ov000_021f1968 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r0
    ldrh r0, [r6]
    mov r5, r1
    bl native_fn_021f3544
    ldrh r1, [r0, #4]
    ldrh r0, [r5]
    mov r1, r1, lsl #16
    mov r4, r1, lsr #17
    bl native_fn_021f3544
    ldrh r2, [r0, #4]
    ldr r0, [r5]
    ldr r1, [r6]
    mov r0, r0, lsr #16
    mov r2, r2, lsl #16
    mov r1, r1, lsr #16
    and r0, r0, #255
    cmp r4, r2, lsr #17
    and r1, r1, #255
    movhi r0, #1
    ldmhiia sp!, {r4, r5, r6, pc}
    cmp r4, r2, lsr #17
    mvnlo r0, #0
    ldmloia sp!, {r4, r5, r6, pc}
    cmp r1, r0
    movhi r0, #1
    ldmhiia sp!, {r4, r5, r6, pc}
    movlo r0, #1
    movhs r0, #0
    rsb r0, r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
