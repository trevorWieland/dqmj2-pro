/* ov001 row 0x021ee7d4: 328 bytes.
 *
 * What it does: 81 instructions; 5 call(s) to 0x02041f74, 0x020299ac, 0x0203d294, +2 more; loops (back edge at +0x24); returns through pop {r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill (81 instructions, 5 calls, 5 branches, 3 back edges, 1 literal slot).
 *
 *   pool +0x144 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x48 -> +0x138
 *   branch +0x60 -> +0x7c
 *   branch +0x78 -> +0xd4
 *   branch +0xd8 -> +0x10c
 *   branch +0x108 -> +0x138
 *   test +0x44 cmp r0, #0
 *   test +0x54 cmp r1, #0
 *   test +0x5c cmplt r1, #0
 *   test +0xd4 cmp r4, #1
 *   2 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021ee7d4; the literal pool and
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

extern void native_fn_02041f74(void);
extern void native_fn_020299ac(void);
extern void native_fn_0203d294(void);
extern void native_fn_02210f64(void);


asm u32 native_ov001_021ee7d4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #28
    mvn r3, #99
    mov r5, r1
    add r1, sp, #16
    mov r6, r0
    mov r4, r2
    str r3, [sp, #0xc]
    str r3, [sp, #0x8]
    bl native_fn_02041f74
    ldr r1, [sp, #0x14]
    add r0, sp, #16
    add r3, r1, #4096
    add r1, sp, #12
    add r2, sp, #8
    str r3, [sp, #0x14]
    bl native_fn_020299ac
    cmp r0, #0
    beq ov001_021ee7d4_L138
    add r0, r6, #768
    ldrsh r1, [r0, #64]
    cmp r1, #0
    ldrltsh r1, [r0, #66]
    cmplt r1, #0
    bge ov001_021ee7d4_L7c
    ldr r1, [sp, #0xc]
    mov r3, #10
    strh r1, [r0, #64]
    ldr r1, [sp, #0x8]
    strh r1, [r0, #66]
    b ov001_021ee7d4_Ld4
ov001_021ee7d4_L7c:
    mov r0, #64
    bl native_fn_0203d294
    add r1, r6, #768
    ldrsh r7, [r1, #64]
    ldr r3, =0x66666667
    mov r2, #5
    add r7, r7, #32
    sub r0, r7, r0
    str r0, [sp, #0xc]
    ldrb r12, [r6, #0x357]
    ldrsh r7, [r1, #66]
    mov r0, r12, lsr #31
    smull r1, r14, r3, r12
    add lr, r0, lr, asr #1
    smull r0, r1, r2, r14
    sub lr, r12, r0
    sub r0, r7, lr, lsl #4
    str r0, [sp, #0x8]
    ldrb r0, [r6, #0x357]
    mov r0, r0, lsl #1
    rsb r0, r0, #12
    and r3, r0, #255
ov001_021ee7d4_Ld4:
    cmp r4, #1
    bne ov001_021ee7d4_L10c
    mov r0, #88
    stmia sp, {r0, r4}
    ldr r1, [sp, #0xc]
    ldr r2, [sp, #0x8]
    mov r0, r5, lsl #16
    mov r1, r1, lsl #16
    mov r2, r2, lsl #16
    mov r0, r0, asr #16
    mov r1, r1, asr #16
    mov r2, r2, asr #16
    bl native_fn_02210f64
    b ov001_021ee7d4_L138
ov001_021ee7d4_L10c:
    mov r0, #89
    stmia sp, {r0, r4}
    ldr r1, [sp, #0xc]
    ldr r2, [sp, #0x8]
    mov r0, r5, lsl #16
    mov r1, r1, lsl #16
    mov r2, r2, lsl #16
    mov r0, r0, asr #16
    mov r1, r1, asr #16
    mov r2, r2, asr #16
    bl native_fn_02210f64
ov001_021ee7d4_L138:
    mov r0, #0
    add sp, sp, #28
    ldmia sp!, {r4, r5, r6, r7, pc}
}
