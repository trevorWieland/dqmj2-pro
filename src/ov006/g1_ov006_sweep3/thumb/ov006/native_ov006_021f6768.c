/* ov006 row 0x021f6768: 156 bytes.
 *
 * What it does: 55 instructions; 12 call(s) to 0x02203fac, 0x021f23a0, 0x021f29bc, +9 more; loops (back edge at +0x12); returns through pop {r3, r4, r5, pc}; 6 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x84 -> native_data_0220b5a2 (image word 0x0220b5a2)
 *   pool +0x88 -> constant 0x0221c0a8 (image word 0x0221c0a8)
 *   pool +0x8c -> native_data_0220b5be (image word 0x0220b5be)
 *   pool +0x90 -> native_data_0220b5bc (image word 0x0220b5bc)
 *   pool +0x94 -> native_data_0220b5c0 (image word 0x0220b5c0)
 *   pool +0x98 -> native_data_0220b5ba (image word 0x0220b5ba)
 *   branch +0x0e -> +0x34
 *   back edge +0x3a -> +0x06
 *   branch +0x44 -> +0x4e
 *   branch +0x56 -> +0x60
 *   branch +0x68 -> +0x72
 *   branch +0x7a -> +0x82
 *   test +0x0c cmp r0, #0x0
 *   test +0x38 cmp r4, #0x3
 *   test +0x42 cmp r0, #0x0
 *   test +0x54 cmp r0, #0x0
 *   test +0x66 cmp r0, #0x0
 *   test +0x78 cmp r0, #0x0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f6768; the literal pool and
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

extern u8 native_data_0220b5a2[];
extern void native_fn_02203fac(void);
extern void native_fn_021f23a0(void);
extern u8 native_data_0220b5be[];
extern u8 native_data_0220b5bc[];
extern u8 native_data_0220b5c0[];
extern u8 native_data_0220b5ba[];
extern void native_fn_021f29bc(void);
extern void native_fn_02203ebc(void);
extern void native_fn_02203eec(void);
extern void native_fn_021f6984(void);


asm u32 native_ov006_021f6768 (register u32 a0)
{
    push {r3, r4, r5, lr}
    ldr r5, =native_data_0220b5a2
    mov r4, #0x0
ov006_021f6768_L6:
    add r0, r5, #0x0
    bl native_fn_02203fac
    cmp r0, #0x0
    beq ov006_021f6768_L34
    mov r0, #0x1
    bl native_fn_021f23a0
    ldr r0, =0x0221c0a8
    ldr r1, =native_data_0220b5be
    strb r4, [r0, #0]
    ldrb r0, [r0, #0]
    ldr r2, =native_data_0220b5bc
    ldr r4, =native_data_0220b5c0
    lsl r3, r0, #0x3
    ldr r0, =native_data_0220b5ba
    ldrh r1, [r1, r3]
    ldrh r0, [r0, r3]
    ldrh r2, [r2, r3]
    ldrh r3, [r4, r3]
    bl native_fn_021f29bc
    pop {r3, r4, r5, pc}
ov006_021f6768_L34:
    add r4, r4, #0x1
    add r5, #0x8
    cmp r4, #0x3
    blo ov006_021f6768_L6
    mov r0, #0x1
    bl native_fn_02203ebc
    cmp r0, #0x0
    beq ov006_021f6768_L4e
    mov r0, #0x1
    bl native_fn_021f23a0
    pop {r3, r4, r5, pc}
ov006_021f6768_L4e:
    mov r0, #0x2
    bl native_fn_02203ebc
    cmp r0, #0x0
    beq ov006_021f6768_L60
    mov r0, #0x0
    bl native_fn_021f23a0
    pop {r3, r4, r5, pc}
ov006_021f6768_L60:
    mov r0, #0x40
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021f6768_L72
    mov r0, #0x1
    bl native_fn_021f6984
    pop {r3, r4, r5, pc}
ov006_021f6768_L72:
    mov r0, #0x80
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021f6768_L82
    mov r0, #0x3
    bl native_fn_021f6984
ov006_021f6768_L82:
    pop {r3, r4, r5, pc}
}
