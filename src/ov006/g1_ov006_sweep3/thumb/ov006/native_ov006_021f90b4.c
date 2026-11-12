/* ov006 row 0x021f90b4: 136 bytes.
 *
 * What it does: 51 instructions; 7 call(s) to 0x021f2f4c, 0x021f52cc, 0x02200344, +4 more; loops (back edge at +0x0e); returns through pop {r3, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x74 -> native_data_0220b65c (image word 0x0220b65c)
 *   pool +0x78 -> constant 0x0221c0e0 (image word 0x0221c0e0)
 *   pool +0x7c -> native_fn_021f913c+1 (image word 0x021f913d)
 *   pool +0x80 -> native_fn_021f9460+1 (image word 0x021f9461)
 *   pool +0x84 -> native_fn_021f92d4+1 (image word 0x021f92d5)
 *   branch +0x14 -> +0x6e
 *   branch +0x20 -> +0x2c
 *   branch +0x2e -> +0x4a
 *   test +0x12 cmp r0, #0x0
 *   test +0x1e cmp r0, #0x0
 *   test +0x2c cmp r0, #0x2
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f90b4; the literal pool and
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

extern u8 native_data_0220b65c[];
extern void native_fn_021f2f4c(void);
extern void native_fn_021f913c(void);
extern void native_fn_021f52cc(void);
extern void native_fn_02200344(void);
extern void native_fn_021f9460(void);
extern void native_fn_021f530c(void);
extern void native_fn_021f92d4(void);


asm u32 native_ov006_021f90b4 (register u32 a0)
{
    push {r3, lr}
    sub sp, #0x10
    ldr r0, =native_data_0220b65c
    ldr r1, [r0, #0x8]
    ldr r0, [r0, #0xc]
    str r1, [sp, #0x8]
    str r0, [sp, #0xc]
    bl native_fn_021f2f4c
    cmp r0, #0x0
    bne ov006_021f90b4_L6e
    ldr r0, =0x0221c0e0
    ldr r0, [r0, #0]
    add r0, #0x2a
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    bne ov006_021f90b4_L2c
    ldr r0, =native_fn_021f913c+1
    bl native_fn_021f52cc
    add sp, #0x10
    pop {r3, pc}
ov006_021f90b4_L2c:
    cmp r0, #0x2
    bne ov006_021f90b4_L4a
    mov r0, #0x0
    mov r2, #0x1
    str r0, [sp]
    mov r0, #0x6
    mov r1, #0x3
    sub r3, r2, #0x2
    bl native_fn_02200344
    ldr r0, =native_fn_021f9460+1
    bl native_fn_021f52cc
    add sp, #0x10
    pop {r3, pc}
ov006_021f90b4_L4a:
    mov r0, #0x0
    add r1, sp, #0x4
    bl native_fn_021f530c
    mov r0, #0x0
    str r0, [sp]
    ldr r0, [sp, #0x4]
    mov r2, #0x1
    lsl r1, r0, #0x2
    add r0, sp, #0x8
    ldr r0, [r0, r1]
    mov r1, #0x2
    sub r3, r2, #0x2
    bl native_fn_02200344
    ldr r0, =native_fn_021f92d4+1
    bl native_fn_021f52cc
ov006_021f90b4_L6e:
    add sp, #0x10
    pop {r3, pc}
    mov r8, r8
}
