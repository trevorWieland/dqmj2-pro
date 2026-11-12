/* ov006 row 0x021efb6c: 80 bytes.
 *
 * What it does: 37 instructions; 3 call(s) to 0x021ef858, 0x021f0744, 0x0201b19c; loops (back edge at +0x0e); returns through pop {r3, r4, r5, r6, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x14 -> +0x1c
 *   branch +0x20 -> +0x28
 *   branch +0x2a -> +0x42
 *   branch +0x40 -> +0x4a
 *   test +0x1e cmp r0, r5
 *   test +0x28 cmp r4, #0x0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021efb6c; the literal pool and
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

extern void native_fn_021ef858(void);
extern void native_fn_021f0744(void);
extern void native_fn_0201b19c(void);


asm u32 native_ov006_021efb6c (register u32 a0)
{
    push {r3, r4, r5, r6, lr}
    sub sp, #0xc
    add r5, r1, #0x0
    add r6, r2, #0x0
    add r1, sp, #0x8
    add r2, sp, #0x4
    add r4, r3, #0x0
    bl native_fn_021ef858
    add r1, r0, #0x0
    bne ov006_021efb6c_L1c
    add sp, #0xc
    mov r0, #0x0
    pop {r3, r4, r5, r6, pc}
ov006_021efb6c_L1c:
    ldr r0, [sp, #0x8]
    cmp r0, r5
    beq ov006_021efb6c_L28
    add sp, #0xc
    mov r0, #0x0
    pop {r3, r4, r5, r6, pc}
ov006_021efb6c_L28:
    cmp r4, #0x0
    beq ov006_021efb6c_L42
    mov r0, #0x10
    str r0, [sp]
    ldr r2, [sp, #0x4]
    add r0, r6, #0x0
    add r3, r4, #0x0
    bl native_fn_021f0744
    ldr r0, [sp, #0x4]
    sub r0, #0x8
    str r0, [sp, #0x4]
    b ov006_021efb6c_L4a
ov006_021efb6c_L42:
    ldr r2, [sp, #0x4]
    add r0, r6, #0x0
    blx native_fn_0201b19c
ov006_021efb6c_L4a:
    ldr r0, [sp, #0x4]
    add sp, #0xc
    pop {r3, r4, r5, r6, pc}
}
