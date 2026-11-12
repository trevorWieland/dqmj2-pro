/* ov006 row 0x021f5bcc: 192 bytes.
 *
 * What it does: 69 instructions; 16 call(s) to 0x02203fac, 0x021f23a0, 0x021f29bc, +13 more; loops (back edge at +0x12); returns through pop {r3, r4, r5, pc}; 6 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xa8 -> native_data_0220b536 (image word 0x0220b536)
 *   pool +0xac -> constant 0x0221c09c (image word 0x0221c09c)
 *   pool +0xb0 -> native_data_0220b54a (image word 0x0220b54a)
 *   pool +0xb4 -> native_data_0220b548 (image word 0x0220b548)
 *   pool +0xb8 -> native_data_0220b54c (image word 0x0220b54c)
 *   pool +0xbc -> native_data_0220b546 (image word 0x0220b546)
 *   branch +0x0e -> +0x34
 *   back edge +0x3a -> +0x06
 *   branch +0x44 -> +0x4e
 *   branch +0x56 -> +0x60
 *   branch +0x68 -> +0x72
 *   branch +0x7a -> +0x84
 *   branch +0x8c -> +0x96
 *   branch +0x9e -> +0xa6
 *   test +0x0c cmp r0, #0x0
 *   test +0x38 cmp r4, #0x2
 *   test +0x42 cmp r0, #0x0
 *   test +0x54 cmp r0, #0x0
 *   test +0x66 cmp r0, #0x0
 *   test +0x78 cmp r0, #0x0
 *   test +0x8a cmp r0, #0x0
 *   test +0x9c cmp r0, #0x0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f5bcc; the literal pool and
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

extern u8 native_data_0220b536[];
extern void native_fn_02203fac(void);
extern void native_fn_021f23a0(void);
extern u8 native_data_0220b54a[];
extern u8 native_data_0220b548[];
extern u8 native_data_0220b54c[];
extern u8 native_data_0220b546[];
extern void native_fn_021f29bc(void);
extern void native_fn_02203ebc(void);
extern void native_fn_02203eec(void);
extern void native_fn_021f5d80(void);


asm u32 native_ov006_021f5bcc (register u32 a0)
{
    push {r3, r4, r5, lr}
    ldr r5, =native_data_0220b536
    mov r4, #0x0
ov006_021f5bcc_L6:
    add r0, r5, #0x0
    bl native_fn_02203fac
    cmp r0, #0x0
    beq ov006_021f5bcc_L34
    mov r0, #0x1
    bl native_fn_021f23a0
    ldr r0, =0x0221c09c
    ldr r1, =native_data_0220b54a
    strb r4, [r0, #0]
    ldrb r0, [r0, #0]
    ldr r2, =native_data_0220b548
    ldr r4, =native_data_0220b54c
    lsl r3, r0, #0x3
    ldr r0, =native_data_0220b546
    ldrh r1, [r1, r3]
    ldrh r0, [r0, r3]
    ldrh r2, [r2, r3]
    ldrh r3, [r4, r3]
    bl native_fn_021f29bc
    pop {r3, r4, r5, pc}
ov006_021f5bcc_L34:
    add r4, r4, #0x1
    add r5, #0x8
    cmp r4, #0x2
    blo ov006_021f5bcc_L6
    mov r0, #0x1
    bl native_fn_02203ebc
    cmp r0, #0x0
    beq ov006_021f5bcc_L4e
    mov r0, #0x1
    bl native_fn_021f23a0
    pop {r3, r4, r5, pc}
ov006_021f5bcc_L4e:
    mov r0, #0x2
    bl native_fn_02203ebc
    cmp r0, #0x0
    beq ov006_021f5bcc_L60
    mov r0, #0x0
    bl native_fn_021f23a0
    pop {r3, r4, r5, pc}
ov006_021f5bcc_L60:
    mov r0, #0x40
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021f5bcc_L72
    mov r0, #0x1
    bl native_fn_021f5d80
    pop {r3, r4, r5, pc}
ov006_021f5bcc_L72:
    mov r0, #0x80
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021f5bcc_L84
    mov r0, #0x3
    bl native_fn_021f5d80
    pop {r3, r4, r5, pc}
ov006_021f5bcc_L84:
    mov r0, #0x20
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021f5bcc_L96
    mov r0, #0x0
    bl native_fn_021f5d80
    pop {r3, r4, r5, pc}
ov006_021f5bcc_L96:
    mov r0, #0x10
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021f5bcc_La6
    mov r0, #0x2
    bl native_fn_021f5d80
ov006_021f5bcc_La6:
    pop {r3, r4, r5, pc}
}
