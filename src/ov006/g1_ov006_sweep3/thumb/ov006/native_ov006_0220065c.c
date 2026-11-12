/* ov006 row 0x0220065c: 212 bytes.
 *
 * What it does: 87 instructions; 9 call(s) to 0x022006b0, 0x022038e8, 0x02203fac, +6 more; loops (back edge at +0x52); returns through pop {r3, r4, r5, r6, r7, pc}; 7 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xb8 -> constant 0x0221c15c (image word 0x0221c15c)
 *   pool +0xbc -> native_data_0220bb3c (image word 0x0220bb3c)
 *   pool +0xc0 -> native_data_0220bb0c (image word 0x0220bb0c)
 *   pool +0xc4 -> native_data_0220ba92 (image word 0x0220ba92)
 *   pool +0xc8 -> native_data_0220bab0 (image word 0x0220bab0)
 *   pool +0xcc -> native_data_0220ba9c (image word 0x0220ba9c)
 *   pool +0xd0 -> native_data_0220ba9d (image word 0x0220ba9d)
 *   branch +0x12 -> +0x54
 *   branch +0x3c -> +0x46
 *   branch +0x44 -> +0x54
 *   back edge +0x52 -> +0x18
 *   branch +0x5c -> +0x6c
 *   branch +0x74 -> +0x84
 *   branch +0x92 -> +0xae
 *   branch +0x9a -> +0xa4
 *   back edge +0xac -> +0x98
 *   test +0x10 cmp r0, #0x0
 *   test +0x3a cmp r0, #0x0
 *   test +0x50 cmp r5, r0
 *   test +0x5a cmp r0, #0x0
 *   test +0x72 cmp r0, #0x0
 *   test +0x90 cmp r2, #0x0
 *   test +0x98 cmp r0, r4
 *   test +0xaa cmp r0, r2
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x0220065c; the literal pool and
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

extern u8 native_data_0220bb3c[];
extern u8 native_data_0220bb0c[];
extern u8 native_data_0220ba92[];
extern u8 native_data_0220bab0[];
extern void native_fn_022038e8(void);
extern void native_fn_02203fac(void);
extern void native_fn_02203ebc(void);
extern u8 native_data_0220ba9c[];
extern u8 native_data_0220ba9d[];
extern void native_fn_022008d0(void);


asm u32 native_ov006_0220065c (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x8
    ldr r0, =0x0221c15c
    ldr r6, =native_data_0220bb3c
    ldr r0, [r0, #0]
    mov r5, #0x0
    ldrb r1, [r0, #0x1c]
    ldrb r0, [r6, r1]
    cmp r0, #0x0
    ble ov006_0220065c_L54
    ldr r7, =native_data_0220bb0c
    add r4, sp, #0x0
ov006_0220065c_L18:
    lsl r0, r1, #0x3
    add r3, r7, r0
    ldr r0, =native_data_0220ba92
    lsl r2, r1, #0x1
    add r0, r0, r2
    ldrb r0, [r5, r0]
    lsl r2, r1, #0x2
    ldr r1, =native_data_0220bab0
    lsl r0, r0, #0x2
    add r1, r1, r2
    add r0, r3, r0
    add r2, r4, #0x0
    bl native_fn_022038e8
    add r0, r4, #0x0
    bl native_fn_02203fac
    cmp r0, #0x0
    beq ov006_0220065c_L46
    ldr r0, =0x0221c15c
    ldr r0, [r0, #0]
    strb r5, [r0, #0x1b]
    b ov006_0220065c_L54
ov006_0220065c_L46:
    ldr r0, =0x0221c15c
    add r5, r5, #0x1
    ldr r0, [r0, #0]
    ldrb r1, [r0, #0x1c]
    ldrb r0, [r6, r1]
    cmp r5, r0
    blt ov006_0220065c_L18
ov006_0220065c_L54:
    mov r0, #0x1
    bl native_fn_02203ebc
    cmp r0, #0x0
    beq ov006_0220065c_L6c
    ldr r0, =0x0221c15c
    ldr r2, [r0, #0]
    ldrb r0, [r2, #0x1c]
    lsl r1, r0, #0x1
    ldr r0, =native_data_0220ba9c
    ldrsb r0, [r0, r1]
    strb r0, [r2, #0x1b]
ov006_0220065c_L6c:
    mov r0, #0x2
    bl native_fn_02203ebc
    cmp r0, #0x0
    beq ov006_0220065c_L84
    ldr r0, =0x0221c15c
    ldr r2, [r0, #0]
    ldrb r0, [r2, #0x1c]
    lsl r1, r0, #0x1
    ldr r0, =native_data_0220ba9d
    ldrsb r0, [r0, r1]
    strb r0, [r2, #0x1b]
ov006_0220065c_L84:
    ldr r1, =0x0221c15c
    ldr r3, =native_data_0220bb3c
    ldr r1, [r1, #0]
    mov r0, #0x0
    ldrb r2, [r1, #0x1c]
    ldrb r2, [r3, r2]
    cmp r2, #0x0
    ble ov006_0220065c_Lae
    mov r2, #0x1b
    ldrsb r4, [r1, r2]
ov006_0220065c_L98:
    cmp r0, r4
    bne ov006_0220065c_La4
    bl native_fn_022008d0
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
ov006_0220065c_La4:
    ldrb r2, [r1, #0x1c]
    add r0, r0, #0x1
    ldrb r2, [r3, r2]
    cmp r0, r2
    blt ov006_0220065c_L98
ov006_0220065c_Lae:
    mov r0, #0x0
    mvn r0, r0
    strb r0, [r1, #0x1b]
    add sp, #0x8
    pop {r3, r4, r5, r6, r7, pc}
}
