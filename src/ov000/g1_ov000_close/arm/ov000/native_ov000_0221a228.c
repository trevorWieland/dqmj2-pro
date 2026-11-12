/* ov000 row 0x0221a228: 120 bytes.
 *
 * What it does: 28 instructions; 2 call(s) to 0x0221a2fc, 0x0221a3a0; no back edge; returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x70 -> constant 0x02246090 (image word 0x02246090)
 *   pool +0x74 -> constant 0x022460c4 (image word 0x022460c4)
 *   branch +0x18 -> +0x38
 *   branch +0x20 -> +0x48
 *   branch +0x34 -> +0x68
 *   branch +0x44 -> +0x68
 *   branch +0x50 -> +0x68
 *   test +0x14 cmp r1, #0
 *   test +0x1c cmp r1, #1
 *   test +0x24 cmp r1, #2
 *   test +0x4c cmp r0, r5
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221a228; the literal pool and
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

extern void native_fn_0221a2fc(void);
extern void native_fn_0221a3a0(void);


asm u32 native_ov000_0221a228 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r0, =0x02246090
    ldr r4, =0x022460c4
    ldr r1, [r0, #0x38]
    ldr r5, [r0, #0x34]
    cmp r1, #0
    beq ov000_0221a228_L38
    cmp r1, #1
    beq ov000_0221a228_L48
    cmp r1, #2
    moveq r0, #0
    ldreq r5, [r4, #0x8]
    streq r0, [r4, #0x4]
    b ov000_0221a228_L68
ov000_0221a228_L38:
    bl native_fn_0221a2fc
    mov r0, #1
    str r0, [r4, #0x4]
    b ov000_0221a228_L68
ov000_0221a228_L48:
    bl native_fn_0221a3a0
    cmp r0, r5
    beq ov000_0221a228_L68
    ldr r2, [r4]
    mov r1, #2
    str r2, [r4, #0xc]
    str r1, [r4, #0x4]
    str r0, [r4, #0x8]
ov000_0221a228_L68:
    mov r0, r5
    ldmia sp!, {r3, r4, r5, pc}
}
