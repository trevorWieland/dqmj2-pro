/* ov006 row 0x02202894: 280 bytes.
 *
 * What it does: 104 instructions; 20 call(s) to 0x02203c08, 0x0200bd04, 0x0200bfe4, +17 more; loops (back edge at +0x12); returns through pop {r4, pc}; 8 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0xf8 -> constant 0x0221c170 (image word 0x0221c170)
 *   pool +0xfc -> native_data_0220e8b0 (image word 0x0220e8b0)
 *   pool +0x100 -> native_data_0220bb44 (image word 0x0220bb44)
 *   pool +0x104 -> native_fn_02202a0c+1 (image word 0x02202a0d)
 *   pool +0x108 -> constant 0x00000602 (image word 0x00000602)
 *   pool +0x10c -> native_fn_02202a48+1 (image word 0x02202a49)
 *   pool +0x110 -> native_fn_02202a7c+1 (image word 0x02202a7d)
 *   pool +0x114 -> native_data_0220e8c8 (image word 0x0220e8c8)
 *   branch +0x20 -> +0x26
 *   branch +0x68 -> +0x6e
 *   branch +0x9e -> +0xa4
 *   test +0x1e cmp r0, #0x0
 *   test +0x66 cmp r0, #0x0
 *   test +0x9c cmp r0, #0x0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02202894; the literal pool and
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

extern void native_fn_02203c08(void);
extern void native_fn_0200bd04(void);
extern u8 native_data_0220e8b0[];
extern void native_fn_0200bfe4(void);
extern void native_fn_02008430(void);
extern void native_fn_020060e4(void);
extern void native_fn_0200c180(void);
extern void native_fn_0200c02c(void);
extern void native_fn_0200b6a8(void);
extern u8 native_data_0220bb44[];
extern void native_fn_0200b714(void);
extern void native_fn_02202a0c(void);
extern void native_fn_0200bc38(void);
extern void native_fn_02202a48(void);
extern void native_fn_02202a7c(void);
extern void native_fn_0200b84c(void);
extern void native_fn_0200b97c(void);
extern void native_fn_022030a4(void);
extern u8 native_data_0220e8c8[];
extern void native_fn_0200616c(void);
extern void native_fn_0200c1fc(void);


asm u32 native_ov006_02202894 (register u32 a0)
{
    push {r4, lr}
    sub sp, #0xe8
    mov r0, #0xe8
    mov r1, #0x4
    bl native_fn_02203c08
    ldr r1, =0x0221c170
    str r0, [r1, #0]
    add r0, sp, #0xa0
    blx native_fn_0200bd04
    ldr r1, =native_data_0220e8b0
    add r0, sp, #0xa0
    blx native_fn_0200bfe4
    cmp r0, #0x0
    bne ov006_02202894_L26
    blx native_fn_02008430
ov006_02202894_L26:
    blx native_fn_020060e4
    ldr r1, =0x0221c170
    mov r2, #0x8
    ldr r1, [r1, #0]
    add r1, #0xe4
    strh r0, [r1, #0]
    add r0, sp, #0xa0
    add r1, sp, #0x18
    ldr r4, [sp, #0xc4]
    blx native_fn_0200c180
    add r0, sp, #0xa0
    add r1, sp, #0x10
    mov r2, #0x8
    blx native_fn_0200c180
    add r0, sp, #0xa0
    blx native_fn_0200c02c
    ldr r0, =0x0221c170
    ldr r0, [r0, #0]
    add r0, #0x88
    blx native_fn_0200b6a8
    ldr r0, =0x0221c170
    ldr r1, =native_data_0220bb44
    ldr r0, [r0, #0]
    mov r2, #0x3
    add r0, #0x88
    blx native_fn_0200b714
    cmp r0, #0x0
    bne ov006_02202894_L6e
    blx native_fn_02008430
ov006_02202894_L6e:
    ldr r0, =0x0221c170
    ldr r1, =native_fn_02202a0c+1
    ldr r0, [r0, #0]
    ldr r2, =0x00000602
    add r0, #0x88
    blx native_fn_0200bc38
    ldr r0, [sp, #0x18]
    add r1, r4, #0x0
    str r0, [sp]
    ldr r0, [sp, #0x1c]
    str r0, [sp, #0x4]
    ldr r0, =native_fn_02202a48+1
    str r0, [sp, #0x8]
    ldr r0, =native_fn_02202a7c+1
    str r0, [sp, #0xc]
    ldr r0, =0x0221c170
    ldr r2, [sp, #0x10]
    ldr r0, [r0, #0]
    ldr r3, [sp, #0x14]
    add r0, #0x88
    blx native_fn_0200b84c
    cmp r0, #0x0
    bne ov006_02202894_La4
    blx native_fn_02008430
ov006_02202894_La4:
    ldr r0, =0x0221c170
    mov r1, #0x0
    ldr r0, [r0, #0]
    add r2, r1, #0x0
    add r0, #0x88
    blx native_fn_0200b97c
    mov r1, #0x4
    add r4, r0, #0x0
    bl native_fn_02203c08
    ldr r1, =0x0221c170
    ldr r2, [r1, #0]
    str r0, [r2, #0]
    ldr r1, [r1, #0]
    add r2, r4, #0x0
    add r0, r1, #0x0
    ldr r1, [r1, #0]
    add r0, #0x88
    blx native_fn_0200b97c
    ldr r1, =0x0221c170
    mov r0, #0x20
    ldr r1, [r1, #0]
    mov r2, #0x4
    add r1, r1, #0x4
    bl native_fn_022030a4
    ldr r1, =0x0221c170
    ldr r2, =native_data_0220bb44
    ldr r1, [r1, #0]
    add r1, #0x84
    str r0, [r1, #0]
    ldr r1, =native_data_0220e8c8
    add r0, sp, #0x20
    blx native_fn_0200616c
    add r0, sp, #0x20
    blx native_fn_0200c1fc
    add sp, #0xe8
    pop {r4, pc}
}
