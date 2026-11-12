/* ov006 row 0x021fe7ec: 128 bytes.
 *
 * What it does: Writes one block of 1 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x74 -> native_data_0220bb60 (image word 0x0220bb60)
 *   pool +0x78 -> constant 0x0221c140 (image word 0x0221c140)
 *   pool +0x7c -> native_data_0220b99c (image word 0x0220b99c)
 *   branch +0x0c -> +0x5c
 *   branch +0x22 -> +0x5c
 *   branch +0x2e -> +0x34
 *   branch +0x32 -> +0x44
 *   branch +0x40 -> +0x44
 *   test +0x0a cmp r0, #0x0
 *   test +0x20 cmp r3, r2
 *   test +0x3e cmp r4, r0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fe7ec; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220bb60[];
extern void native_fn_02203f4c(void);
extern void native_fn_0220410c(void);
extern u8 native_data_0220b99c[];
extern void native_fn_021fe86c(void);
extern void native_fn_021fea34(void);
extern void native_fn_021ff718(void);


asm u32 native_ov006_021fe7ec (register u32 a0)
{
    push {r3, r4, lr}
    sub sp, #0x4
    ldr r0, =native_data_0220bb60
    bl native_fn_02203f4c
    cmp r0, #0x0
    beq ov006_021fe7ec_L5c
    add r0, sp, #0x0
    bl native_fn_0220410c
    ldr r0, =0x0221c140
    add r1, sp, #0x0
    ldr r0, [r0, #0]
    ldrh r3, [r1, #0]
    ldrh r2, [r0, #0x10]
    sub r2, #0x1e
    cmp r3, r2
    blt ov006_021fe7ec_L5c
    ldrh r2, [r1, #0x2]
    ldrh r1, [r0, #0x16]
    ldrb r3, [r0, #0x18]
    sub r1, r2, r1
    add r4, r3, r1
    bpl ov006_021fe7ec_L34
    mov r4, #0x0
    b ov006_021fe7ec_L44
ov006_021fe7ec_L34:
    ldrb r1, [r0, #0x1b]
    ldrb r2, [r0, #0x19]
    ldr r0, =native_data_0220b99c
    ldrb r0, [r0, r1]
    sub r0, r2, r0
    cmp r4, r0
    blt ov006_021fe7ec_L44
    add r4, r0, #0x0
ov006_021fe7ec_L44:
    add r0, r4, #0x0
    bl native_fn_021fe86c
    add r0, r4, #0x0
    bl native_fn_021fea34
    ldr r0, =0x0221c140
    mov r1, #0x2
    ldr r0, [r0, #0]
    add sp, #0x4
    strb r1, [r0, #0x1d]
    pop {r3, r4, pc}
ov006_021fe7ec_L5c:
    bl native_fn_021ff718
    ldr r0, =0x0221c140
    mov r2, #0x0
    ldr r1, [r0, #0]
    strb r2, [r1, #0x1c]
    ldr r0, [r0, #0]
    mov r1, #0x3
    strb r1, [r0, #0x1d]
    add sp, #0x4
    pop {r3, r4, pc}
    mov r8, r8
}
