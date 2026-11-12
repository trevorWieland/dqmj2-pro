/* ov006 row 0x021fcab0: 156 bytes.
 *
 * What it does: 59 instructions; 16 call(s) to 0x02203fac, 0x021f23a0, 0x021fcdb4, +13 more; loops (back edge at +0x12); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x94 -> native_data_0220b842 (image word 0x0220b842)
 *   pool +0x98 -> constant 0x0221c10c (image word 0x0221c10c)
 *   branch +0x0e -> +0x20
 *   back edge +0x26 -> +0x06
 *   branch +0x30 -> +0x3a
 *   branch +0x42 -> +0x4c
 *   branch +0x54 -> +0x5e
 *   branch +0x66 -> +0x70
 *   branch +0x78 -> +0x82
 *   branch +0x8a -> +0x92
 *   test +0x0c cmp r0, #0x0
 *   test +0x24 cmp r4, #0x7
 *   test +0x2e cmp r0, #0x0
 *   test +0x40 cmp r0, #0x0
 *   test +0x52 cmp r0, #0x0
 *   test +0x64 cmp r0, #0x0
 *   test +0x76 cmp r0, #0x0
 *   test +0x88 cmp r0, #0x0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fcab0; the literal pool and
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

extern u8 native_data_0220b842[];
extern void native_fn_02203fac(void);
extern void native_fn_021f23a0(void);
extern void native_fn_021fcdb4(void);
extern void native_fn_02203ebc(void);
extern void native_fn_02203eec(void);
extern void native_fn_021fce00(void);


asm u32 native_ov006_021fcab0 (register u32 a0)
{
    push {r3, r4, r5, lr}
    ldr r5, =native_data_0220b842
    mov r4, #0x0
ov006_021fcab0_L6:
    add r0, r5, #0x0
    bl native_fn_02203fac
    cmp r0, #0x0
    beq ov006_021fcab0_L20
    mov r0, #0x1
    bl native_fn_021f23a0
    ldr r0, =0x0221c10c
    strb r4, [r0, #0]
    bl native_fn_021fcdb4
    pop {r3, r4, r5, pc}
ov006_021fcab0_L20:
    add r4, r4, #0x1
    add r5, #0x8
    cmp r4, #0x7
    blo ov006_021fcab0_L6
    mov r0, #0x1
    bl native_fn_02203ebc
    cmp r0, #0x0
    beq ov006_021fcab0_L3a
    mov r0, #0x1
    bl native_fn_021f23a0
    pop {r3, r4, r5, pc}
ov006_021fcab0_L3a:
    mov r0, #0x2
    bl native_fn_02203ebc
    cmp r0, #0x0
    beq ov006_021fcab0_L4c
    mov r0, #0x0
    bl native_fn_021f23a0
    pop {r3, r4, r5, pc}
ov006_021fcab0_L4c:
    mov r0, #0x40
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021fcab0_L5e
    mov r0, #0x1
    bl native_fn_021fce00
    pop {r3, r4, r5, pc}
ov006_021fcab0_L5e:
    mov r0, #0x80
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021fcab0_L70
    mov r0, #0x3
    bl native_fn_021fce00
    pop {r3, r4, r5, pc}
ov006_021fcab0_L70:
    mov r0, #0x20
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021fcab0_L82
    mov r0, #0x0
    bl native_fn_021fce00
    pop {r3, r4, r5, pc}
ov006_021fcab0_L82:
    mov r0, #0x10
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021fcab0_L92
    mov r0, #0x2
    bl native_fn_021fce00
ov006_021fcab0_L92:
    pop {r3, r4, r5, pc}
}
