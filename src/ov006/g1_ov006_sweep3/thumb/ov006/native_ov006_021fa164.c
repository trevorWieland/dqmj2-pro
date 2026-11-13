/* ov006 row 0x021fa164: 336 bytes.
 *
 * What it does: 136 instructions; 21 call(s) to 0x021fedc8, 0x02203c08, 0x021fa3f8, +18 more; loops (back edge at +0x38); returns through pop {r3, r4, r5, r6, r7, pc}; 6 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x138 -> constant 0x0221c0ec (image word 0x0221c0ec)
 *   pool +0x13c -> native_data_0220b7dc (image word 0x0220b7dc)
 *   pool +0x140 -> constant 0xfffff3ff (image word 0xfffff3ff)
 *   pool +0x144 -> native_fn_021fb474+1 (image word 0x021fb475)
 *   pool +0x148 -> native_fn_021fb7d0+1 (image word 0x021fb7d1)
 *   pool +0x14c -> native_fn_021fa41c+1 (image word 0x021fa41d)
 *   branch +0x36 -> +0x52
 *   branch +0x50 -> +0x5e
 *   back edge +0xac -> +0x98
 *   branch +0xb8 -> +0xc0
 *   branch +0xbc -> +0xe2
 *   branch +0xbe -> +0x102
 *   branch +0xe0 -> +0x102
 *   test +0x34 cmp r0, #0x0
 *   test +0xaa cmp r4, #0x7
 *   test +0xb6 cmp r0, #0x1
 *   test +0xba cmp r0, #0x2
 *   0 block transfer(s), 14 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fa164; the literal pool and
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
extern void ov006_clear_buffer_02203c08(void);
extern void native_fn_021fa3f8(void);
extern void native_fn_021fa2b4(void);
extern void native_fn_021f5328(void);
extern u8 native_data_0220b7dc[];
extern void native_fn_021f26f0(void);
extern void native_fn_021f27fc(void);
extern void native_fn_021f2b28(void);
extern void native_fn_02026144(void);
extern void native_fn_021fe60c(void);
extern void native_fn_022034dc(void);
extern void native_fn_0220303c(void);
extern void native_fn_021fb474(void);
extern void native_fn_0220490c(void);
extern void native_fn_021fb7d0(void);
extern void native_fn_021fabe4(void);
extern void native_fn_021fb4cc(void);
extern void native_fn_021fa41c(void);
extern void ov006_main_loop_set_callback_021f52cc(void);


asm u32 native_ov006_021fa164 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x8
    bl native_fn_021fedc8
    str r0, [sp, #0x4]
    mov r0, #0x48
    mov r1, #0x4
    bl ov006_clear_buffer_02203c08
    ldr r2, =0x0221c0ec
    ldr r1, [sp, #0x4]
    str r0, [r2, #0x8]
    add r1, #0xf6
    ldrb r1, [r1, #0]
    add r0, #0x43
    strb r1, [r0, #0]
    ldr r0, [r2, #0x8]
    mov r1, #0xc
    add r0, #0x42
    strb r1, [r0, #0]
    bl native_fn_021fa3f8
    bl native_fn_021fa2b4
    ldr r0, =0x0221c0ec
    ldrb r0, [r0, #0x1]
    cmp r0, #0x0
    bne ov006_021fa164_L52
    bl native_fn_021f5328
    add r2, r0, #0x0
    ldr r1, =native_data_0220b7dc
    mov r0, #0x30
    ldrsb r1, [r1, r2]
    ldr r2, [sp, #0x4]
    add r2, #0xf4
    ldrb r2, [r2, #0]
    add r2, r2, #0x1
    bl native_fn_021f26f0
    b ov006_021fa164_L5e
ov006_021fa164_L52:
    mov r0, #0x45
    add r1, r0, #0x0
    sub r1, #0x46
    mov r2, #0x0
    bl native_fn_021f26f0
ov006_021fa164_L5e:
    mov r0, #0x1
    bl native_fn_021f27fc
    bl native_fn_021f2b28
    ldr r0, =0x0221c0ec
    ldrh r1, [r0, #0x4]
    mov r0, #0x37
    mul r0, r1
    mov r1, #0x91
    blx native_fn_02026144
    str r0, [sp]
    mov r0, #0x2
    mov r1, #0x55
    mov r2, #0xf1
    mov r3, #0x41
    bl native_fn_021fe60c
    mov r0, #0x0
    mov r1, #0x1
    bl native_fn_022034dc
    mov r4, #0x0
    ldr r6, =0x0221c0ec
    add r5, r4, #0x0
    ldr r1, [r6, #0x8]
    add r7, r4, #0x0
    str r0, [r1, #0x14]
ov006_021fa164_L98:
    add r0, r7, #0x0
    mov r1, #0x29
    bl native_fn_0220303c
    ldr r1, [r6, #0x8]
    add r4, r4, #0x1
    add r1, r1, r5
    add r5, r5, #0x4
    str r0, [r1, #0x18]
    cmp r4, #0x7
    blt ov006_021fa164_L98
    ldr r0, [sp, #0x4]
    add r0, #0xe7
    str r0, [sp, #0x4]
    ldrb r0, [r0, #0]
    cmp r0, #0x1
    beq ov006_021fa164_Lc0
    cmp r0, #0x2
    beq ov006_021fa164_Le2
    b ov006_021fa164_L102
ov006_021fa164_Lc0:
    mov r0, #0x0
    mov r1, #0x50
    bl native_fn_0220303c
    ldr r1, =0x0221c0ec
    ldr r2, [r1, #0x8]
    str r0, [r2, #0x34]
    ldr r0, [r1, #0x8]
    ldr r2, [r0, #0x34]
    ldr r0, =0xfffff3ff
    ldrh r1, [r2, #0x4]
    and r1, r0
    mov r0, #0x3
    lsl r0, r0, #0xa
    orr r0, r1
    strh r0, [r2, #0x4]
    b ov006_021fa164_L102
ov006_021fa164_Le2:
    mov r0, #0x0
    mov r1, #0x51
    bl native_fn_0220303c
    ldr r1, =0x0221c0ec
    ldr r2, [r1, #0x8]
    str r0, [r2, #0x34]
    ldr r0, [r1, #0x8]
    ldr r2, [r0, #0x34]
    ldr r0, =0xfffff3ff
    ldrh r1, [r2, #0x4]
    and r1, r0
    mov r0, #0x3
    lsl r0, r0, #0xa
    orr r0, r1
    strh r0, [r2, #0x4]
ov006_021fa164_L102:
    ldr r1, =native_fn_021fb474+1
    mov r0, #0x1
    mov r2, #0x0
    mov r3, #0x6e
    bl native_fn_0220490c
    ldr r1, =0x0221c0ec
    mov r3, #0x78
    ldr r1, [r1, #0x8]
    str r0, [r1, #0x3c]
    mov r0, #0x0
    ldr r1, =native_fn_021fb7d0+1
    add r2, r0, #0x0
    bl native_fn_0220490c
    ldr r1, =0x0221c0ec
    ldr r1, [r1, #0x8]
    str r0, [r1, #0]
    bl native_fn_021fabe4
    bl native_fn_021fb4cc
    ldr r0, =native_fn_021fa41c+1
    bl ov006_main_loop_set_callback_021f52cc
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
}
