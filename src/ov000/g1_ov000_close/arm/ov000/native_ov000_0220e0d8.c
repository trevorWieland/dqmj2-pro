/* ov000 row 0x0220e0d8: 308 bytes.
 *
 * What it does: 77 instructions; 5 call(s) to 0x021e07b8, 0x021e6040, 0x0220e1e4, +2 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x74 -> +0x10c
 *   branch +0xb0 -> +0x104
 *   branch +0xf0 -> +0x104
 *   branch +0x100 -> +0x10c
 *   back edge +0x108 -> +0x64
 *   branch +0x110 -> +0x128
 *   test +0x70 cmp r0, #0
 *   test +0xf8 cmp r5, #16
 *   test +0x10c cmp r5, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220e0d8; the literal pool and
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

extern void native_fn_021e07b8(void);
extern void native_fn_021e6040(void);
extern void native_fn_0203d294(void);


asm u32 native_ov000_0220e0d8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #32
    mov r8, r0
    mvn r1, #0
    mov r0, #0
    str r1, [sp]
    bl native_fn_021e07b8
    mov r6, r0
    ldr r1, [r6, #0x4]
    ldr r0, [r8, #0x74]
    ldr r2, [r6]
    sub r3, r1, r0
    ldr r1, [r8, #0x70]
    smull r0, r4, r3, r3
    sub r1, r2, r1
    smlal r0, r4, r1, r1
    ldr r2, [r6, #0x8]
    ldr r1, [r8, #0x78]
    mov r5, #0
    sub r1, r2, r1
    smlal r0, r4, r1, r1
    mov r11, r0, lsr #12
    add r7, sp, #16
    mov r0, r5
    orr r11, r11, r4, lsl #20
ov000_0220e0d8_L64:
    ldrb r2, [r8, #0x2c0]
    add r1, sp, #4
    bl native_fn_021e6040
    cmp r0, #0
    blt ov000_0220e0d8_L10c
    ldr r2, [sp, #0x4]
    ldr r1, [r8, #0x2a8]
    ldr r12, [r8, #0x2b8]
    sub r1, r1, r2
    smull r9, r14, r1, r1
    ldr r1, [sp, #0xc]
    ldr r10, [r8, #0x2b0]
    mov r3, r12, asr #31
    sub r10, r10, r1
    smlal r9, lr, r10, r10
    mov r9, r9, lsr #12
    orr r9, r9, lr, lsl #20
    subs r9, r9, r12
    rscs r9, r3, lr, asr #12
    bge ov000_0220e0d8_L104
    ldr r9, [r6, #0x4]
    ldr r3, [sp, #0x8]
    ldr r10, [r6]
    sub r12, r9, r3
    smull r9, r3, r12, r12
    sub r2, r10, r2
    smlal r9, r3, r2, r2
    ldr r2, [r6, #0x8]
    sub r1, r2, r1
    smlal r9, r3, r1, r1
    mov r1, r9, lsr #12
    orr r1, r1, r3, lsl #20
    mov r2, r3, asr #12
    subs r1, r11, r1
    rscs r1, r2, r4, asr #12
    bge ov000_0220e0d8_L104
    add r5, r5, #1
    cmp r5, #16
    strb r0, [r7], #1
    bge ov000_0220e0d8_L10c
ov000_0220e0d8_L104:
    add r0, r0, #1
    b ov000_0220e0d8_L64
ov000_0220e0d8_L10c:
    cmp r5, #0
    ble ov000_0220e0d8_L128
    mov r0, r5
    bl native_fn_0203d294
    add r1, sp, #16
    ldrb r0, [r1, r0]
    str r0, [sp]
ov000_0220e0d8_L128:
    ldr r0, [sp]
    add sp, sp, #32
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
