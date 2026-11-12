/* ov006 row 0x0220374c: 116 bytes.
 *
 * What it does: 51 instructions; 3 call(s) to 0x0203694c, 0x02036994, 0x02203720; loops (back edge at +0x24); returns through pop {r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x6c -> constant 0x0221c184 (image word 0x0221c184)
 *   pool +0x70 -> constant 0x0000ffff (image word 0x0000ffff)
 *   branch +0x1a -> +0x66
 *   branch +0x2e -> +0x34
 *   back edge +0x64 -> +0x1e
 *   test +0x18 cmp r1, #0x0
 *   test +0x2c cmp r1, r0
 *   test +0x62 cmp r1, #0x0
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x0220374c; the literal pool and
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

extern void native_fn_0203694c(void);
extern void native_fn_02036994(void);
extern void native_fn_02203720(void);


asm u32 native_ov006_0220374c (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0x14
    ldr r5, [sp, #0x2c]
    str r0, [sp, #0x8]
    ldr r0, [sp, #0x28]
    add r6, r1, #0x0
    ldrh r1, [r5, #0]
    str r0, [sp, #0x28]
    ldr r0, [sp, #0x30]
    str r2, [sp, #0xc]
    str r3, [sp, #0x10]
    str r0, [sp, #0x30]
    cmp r1, #0x0
    beq ov006_0220374c_L66
    lsl r4, r0, #0x3
ov006_0220374c_L1e:
    ldr r0, =0x0221c184
    ldr r7, [r0, #0]
    add r0, r7, r4
    blx native_fn_0203694c
    add r1, r0, #0x0
    ldr r0, =0x0000ffff
    cmp r1, r0
    bne ov006_0220374c_L34
    ldr r0, [r7, r4]
    ldrh r1, [r0, #0x2]
ov006_0220374c_L34:
    add r0, r7, r4
    blx native_fn_02036994
    add r1, r0, #0x0
    ldrh r0, [r5, #0]
    mov r2, #0x2
    ldr r3, [sp, #0x10]
    str r0, [sp]
    ldr r0, [sp, #0x30]
    str r0, [sp, #0x4]
    ldrsb r2, [r1, r2]
    ldr r1, [sp, #0x28]
    ldr r0, [sp, #0x8]
    sub r1, r1, r2
    asr r1, r1, #0x1
    ldr r2, [sp, #0xc]
    add r1, r6, r1
    bl native_fn_02203720
    add r5, r5, #0x2
    ldr r0, [sp, #0x28]
    ldrh r1, [r5, #0]
    add r6, r6, r0
    cmp r1, #0x0
    bne ov006_0220374c_L1e
ov006_0220374c_L66:
    add sp, #0x14
    pop {r4, r5, r6, r7, pc}
    mov r8, r8
}
