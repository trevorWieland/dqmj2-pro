/* ov006 row 0x021f6294: 340 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x144 -> native_data_0220dc18 (image word 0x0220dc18)
 *   pool +0x148 -> constant 0x00002710 (image word 0x00002710)
 *   pool +0x14c -> native_data_0220dc38 (image word 0x0220dc38)
 *   pool +0x150 -> native_data_0220dc4c (image word 0x0220dc4c)
 *   branch +0x7a -> +0xfe
 *   back edge +0xd2 -> +0xa8
 *   branch +0xfc -> +0x118
 *   test +0xd0 cmp r5, #0x3
 *   0 block transfer(s), 19 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f6294; the literal pool and
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

extern void native_fn_022034dc(void);
extern void native_fn_020081fc(void);
extern u8 native_data_0220dc18[];
extern void native_fn_020061ac(void);
extern void native_fn_022045e0(void);
extern void native_fn_022037c0(void);
extern void native_fn_020a4660(void);
extern void native_fn_020260e8(void);
extern void native_fn_02026124(void);
extern void native_fn_020260dc(void);
extern u8 native_data_0220dc38[];
extern u8 native_data_0220dc4c[];
extern void native_fn_022038ac(void);


asm u32 native_ov006_021f6294 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x80
    mov r0, #0x0
    add r1, r0, #0x0
    bl native_fn_022034dc
    str r0, [sp, #0x14]
    add r0, sp, #0x18
    blx native_fn_020081fc
    add r3, sp, #0x18
    ldrb r0, [r3, #0x1]
    ldr r2, =native_data_0220dc18
    mov r1, #0x14
    str r0, [sp]
    ldrb r0, [r3, #0x2]
    str r0, [sp, #0x4]
    ldrb r0, [r3, #0x3]
    str r0, [sp, #0x8]
    ldrb r0, [r3, #0x4]
    str r0, [sp, #0xc]
    ldrb r0, [r3, #0x5]
    str r0, [sp, #0x10]
    add r0, sp, #0x1c
    ldrb r3, [r3, #0]
    add r0, #0x2
    blx native_fn_020061ac
    add r0, sp, #0x30
    add r1, sp, #0x1c
    add r0, #0x2
    add r1, #0x2
    mov r2, #0x14
    bl native_fn_022045e0
    mov r0, #0x1c
    str r0, [sp]
    mov r0, #0x2
    str r0, [sp, #0x4]
    mov r0, #0x12
    lsl r0, r0, #0x6
    str r0, [sp, #0x8]
    add r0, sp, #0x30
    add r0, #0x2
    str r0, [sp, #0xc]
    ldr r0, [sp, #0x14]
    mov r1, #0x8
    mov r2, #0x40
    mov r3, #0xf0
    bl native_fn_022037c0
    add r0, sp, #0x6c
    bl native_fn_020a4660
    ldr r4, [sp, #0x6c]
    mov r0, #0x0
    ldr r6, [sp, #0x70]
    mov r1, #0x0
    eor r1, r6
    eor r0, r4
    orr r0, r1
    beq ov006_021f6294_Lfe
    add r0, r4, #0x0
    add r1, r6, #0x0
    mov r2, #0xa
    mov r3, #0x0
    blx native_fn_020260e8
    mov r2, #0xfa
    lsl r2, r2, #0x2
    mov r3, #0x0
    blx native_fn_02026124
    str r0, [sp, #0x68]
    add r0, r4, #0x0
    add r1, r6, #0x0
    mov r2, #0xa
    mov r3, #0x0
    blx native_fn_020260dc
    ldr r7, =0x00002710
    add r4, r0, #0x0
    add r6, r1, #0x0
    mov r5, #0x0
ov006_021f6294_La8:
    add r0, r4, #0x0
    add r1, r6, #0x0
    add r2, r7, #0x0
    mov r3, #0x0
    blx native_fn_020260e8
    mov r1, #0x2
    sub r1, r1, r5
    lsl r2, r1, #0x2
    add r1, sp, #0x5c
    str r0, [r1, r2]
    add r0, r4, #0x0
    add r1, r6, #0x0
    add r2, r7, #0x0
    mov r3, #0x0
    blx native_fn_020260dc
    add r5, r5, #0x1
    add r4, r0, #0x0
    add r6, r1, #0x0
    cmp r5, #0x3
    blt ov006_021f6294_La8
    ldr r0, [sp, #0x60]
    ldr r2, =native_data_0220dc38
    str r0, [sp]
    ldr r0, [sp, #0x64]
    ldr r3, [sp, #0x5c]
    str r0, [sp, #0x4]
    ldr r0, [sp, #0x68]
    mov r1, #0x14
    str r0, [sp, #0x8]
    add r0, sp, #0x1c
    add r0, #0x2
    blx native_fn_020061ac
    add r0, sp, #0x30
    add r1, sp, #0x1c
    add r0, #0x2
    add r1, #0x2
    mov r2, #0x14
    bl native_fn_022045e0
    b ov006_021f6294_L118
ov006_021f6294_Lfe:
    add r0, sp, #0x1c
    ldr r2, =native_data_0220dc4c
    add r0, #0x2
    mov r1, #0x14
    blx native_fn_020061ac
    add r0, sp, #0x30
    add r1, sp, #0x1c
    add r0, #0x2
    add r1, #0x2
    mov r2, #0x14
    bl native_fn_022045e0
ov006_021f6294_L118:
    mov r0, #0x1c
    str r0, [sp]
    mov r0, #0x2
    str r0, [sp, #0x4]
    mov r0, #0x12
    lsl r0, r0, #0x6
    str r0, [sp, #0x8]
    add r0, sp, #0x30
    add r0, #0x2
    str r0, [sp, #0xc]
    ldr r0, [sp, #0x14]
    mov r1, #0x8
    mov r2, #0x78
    mov r3, #0xf0
    bl native_fn_022037c0
    ldr r0, [sp, #0x14]
    bl native_fn_022038ac
    add sp, #0x80
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
