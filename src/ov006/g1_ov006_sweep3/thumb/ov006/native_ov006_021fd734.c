/* ov006 row 0x021fd734: 112 bytes.
 *
 * What it does: 44 instructions; 6 call(s) to 0x021fedc8, 0x02008c28, 0x021f530c, +3 more; loops (back edge at +0x10); returns through pop {r4, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x64 -> native_data_0220b980 (image word 0x0220b980)
 *   pool +0x68 -> constant 0x0221c11c (image word 0x0221c11c)
 *   pool +0x6c -> native_fn_021fd8d8+1 (image word 0x021fd8d9)
 *   branch +0x20 -> +0x26
 *   branch +0x24 -> +0x2e
 *   branch +0x3e -> +0x52
 *   branch +0x44 -> +0x52
 *   test +0x1e cmp r0, #0x2
 *   test +0x3a cmp r0, #0x0
 *   test +0x42 cmp r0, #0x0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fd734; the literal pool and
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

extern void native_fn_021fedc8(void);
extern u8 native_data_0220b980[];
extern void native_fn_02008c28(void);
extern void native_fn_021f530c(void);
extern void native_fn_02094284(void);
extern void native_fn_020945bc(void);
extern void native_fn_021fd8d8(void);
extern void native_fn_0220490c(void);


asm u32 native_ov006_021fd734 (register u32 a0)
{
    push {r4, lr}
    sub sp, #0x10
    bl native_fn_021fedc8
    add r4, r0, #0x0
    ldr r0, =native_data_0220b980
    add r1, sp, #0x4
    mov r2, #0xc
    blx native_fn_02008c28
    mov r0, #0x0
    add r1, sp, #0x0
    bl native_fn_021f530c
    ldr r0, [sp]
    cmp r0, #0x2
    bne ov006_021fd734_L26
    mov r1, #0x4
    b ov006_021fd734_L2e
ov006_021fd734_L26:
    add r0, r4, #0x0
    add r0, #0xf4
    ldrb r0, [r0, #0]
    add r1, r0, #0x1
ov006_021fd734_L2e:
    add r0, sp, #0x0
    strb r1, [r0, #0xe]
    add r0, sp, #0x4
    bl native_fn_02094284
    ldr r1, =0x0221c11c
    cmp r0, #0x0
    str r0, [r1, #0x4]
    beq ov006_021fd734_L52
    ldr r0, [sp]
    cmp r0, #0x0
    bne ov006_021fd734_L52
    add r0, r4, #0x0
    add r0, #0xf4
    ldrb r0, [r0, #0]
    add r1, r4, #0x0
    bl native_fn_020945bc
ov006_021fd734_L52:
    mov r0, #0x0
    ldr r1, =native_fn_021fd8d8+1
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    add sp, #0x10
    pop {r4, pc}
    mov r8, r8
}
