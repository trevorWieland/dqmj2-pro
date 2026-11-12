/* ov000 row 0x0220aa0c: 92 bytes.
 *
 * What it does: 23 instructions; 2 call(s) to 0x0220aa60, 0x0200235c; loops (back edge at +0x2c); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x10 -> +0x54
 *   branch +0x24 -> +0x54
 *   test +0x08 cmp r5, #655360
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220aa0c; the literal pool and
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

extern void native_fn_0200235c(void);


asm u32 native_ov000_0220aa0c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r5, r0
    cmp r5, #655360
    ldr r0, [sp, #0x10]
    bge ov000_0220aa0c_L54
    subs r4, r1, r3
    sbc r6, r2, r0
    subs r0, r4, #0
    sbcs r0, r6, #0
    blt ov000_0220aa0c_L54
    rsb r0, r5, #655360
    bl native_fn_0200235c
    umull r2, r1, r0, r4
    mla r1, r0, r6, r1
    mov r0, r0, asr #31
    adds r2, r2, #2048
    mla r1, r0, r4, r1
    adc r0, r1, #0
    mov r1, r2, lsr #12
    orr r1, r1, r0, lsl #20
    add r5, r1, r5
ov000_0220aa0c_L54:
    mov r0, r5
    ldmia sp!, {r4, r5, r6, pc}
}
