/* ov006 row 0x02200770: 280 bytes.
 *
 * What it does: 118 instructions; 12 call(s) to 0x02202eb0, 0x02202eb0, 0x02200888, +9 more; loops (back edge at +0xbc); returns through pop {r3, r4, r5, r6, r7, pc}; 7 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xfc -> constant 0x0221c15c (image word 0x0221c15c)
 *   pool +0x100 -> native_data_0220badc (image word 0x0220badc)
 *   pool +0x104 -> native_data_0220bb3c (image word 0x0220bb3c)
 *   pool +0x108 -> native_data_0220bb0c (image word 0x0220bb0c)
 *   pool +0x10c -> native_data_0220ba92 (image word 0x0220ba92)
 *   pool +0x110 -> native_data_0220baf6 (image word 0x0220baf6)
 *   pool +0x114 -> native_data_0220baf4 (image word 0x0220baf4)
 *   branch +0x60 -> +0xbe
 *   back edge +0xbc -> +0x64
 *   branch +0xc4 -> +0xcc
 *   branch +0xca -> +0xd4
 *   branch +0xd6 -> +0xda
 *   test +0x5e cmp r0, #0x0
 *   test +0xba cmp r4, r0
 *   test +0xc2 cmp r1, #0xc0
 *   test +0xd4 cmp r3, #0xc0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02200770; the literal pool and
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

extern u8 native_data_0220badc[];
extern void native_fn_02202eb0(void);
extern void native_fn_02200888(void);
extern u8 native_data_0220bb3c[];
extern u8 native_data_0220bb0c[];
extern u8 native_data_0220ba92[];
extern u8 native_data_0220baf6[];
extern u8 native_data_0220baf4[];
extern void native_fn_022038d8(void);
extern void native_fn_022039a4(void);


asm u32 native_ov006_02200770 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x10
    add r7, r0, #0x0
    ldr r0, =0x0221c15c
    mov r1, #0x0
    ldr r2, [r0, #0]
    mvn r1, r1
    ldr r0, [r2, #0]
    ldrb r2, [r2, #0x1c]
    lsl r3, r2, #0x2
    ldr r2, =native_data_0220badc
    ldrh r2, [r2, r3]
    add r3, r7, #0x0
    bl native_fn_02202eb0
    ldr r0, =0x0221c15c
    mov r1, #0x0
    ldr r2, [r0, #0]
    mvn r1, r1
    ldr r0, [r2, #0x4]
    ldrb r2, [r2, #0x1c]
    lsl r3, r2, #0x2
    ldr r2, =native_data_0220badc
    ldrh r2, [r2, r3]
    add r3, r7, #0x0
    add r3, #0x8
    add r2, #0x8
    bl native_fn_02202eb0
    ldr r0, =0x0221c15c
    add r1, r7, #0x0
    ldr r0, [r0, #0]
    ldr r0, [r0, #0]
    bl native_fn_02200888
    ldr r0, =0x0221c15c
    add r1, r7, #0x0
    ldr r0, [r0, #0]
    ldr r0, [r0, #0x4]
    bl native_fn_02200888
    ldr r0, =0x0221c15c
    mov r4, #0x0
    ldr r0, [r0, #0]
    ldrb r5, [r0, #0x1c]
    ldr r0, =native_data_0220bb3c
    ldrb r0, [r0, r5]
    cmp r0, #0x0
    ble ov006_02200770_Lbe
    add r6, r4, #0x0
ov006_02200770_L64:
    ldr r1, =native_data_0220bb0c
    lsl r2, r5, #0x3
    add r3, r1, r2
    lsl r2, r5, #0x1
    ldr r1, =native_data_0220ba92
    ldr r0, =0x0221c15c
    add r1, r1, r2
    ldrb r1, [r4, r1]
    ldr r0, [r0, #0]
    lsl r5, r5, #0x2
    lsl r2, r1, #0x2
    add r1, r3, r2
    str r1, [sp, #0x4]
    ldrh r2, [r3, r2]
    ldr r3, [sp, #0x4]
    add r0, r0, r6
    ldrh r3, [r3, #0x2]
    mov r1, #0x0
    ldr r0, [r0, #0x8]
    add r3, r7, r3
    mov r12, r3
    ldr r3, =native_data_0220badc
    mvn r1, r1
    add r3, r3, r5
    ldrh r3, [r3, #0x2]
    mov r5, r12
    sub r3, r5, r3
    bl native_fn_02202eb0
    ldr r0, =0x0221c15c
    add r1, r7, #0x0
    ldr r0, [r0, #0]
    add r0, r0, r6
    ldr r0, [r0, #0x8]
    bl native_fn_02200888
    ldr r0, =0x0221c15c
    add r4, r4, #0x1
    ldr r0, [r0, #0]
    add r6, r6, #0x4
    ldrb r5, [r0, #0x1c]
    ldr r0, =native_data_0220bb3c
    ldrb r0, [r0, r5]
    cmp r4, r0
    blt ov006_02200770_L64
ov006_02200770_Lbe:
    lsl r0, r7, #0x18
    lsr r1, r0, #0x18
    cmp r1, #0xc0
    blt ov006_02200770_Lcc
    mov r3, #0x0
    add r1, r3, #0x0
    b ov006_02200770_Ld4
ov006_02200770_Lcc:
    ldr r0, =native_data_0220baf6
    lsl r2, r5, #0x2
    ldrh r0, [r0, r2]
    add r3, r1, r0
ov006_02200770_Ld4:
    cmp r3, #0xc0
    ble ov006_02200770_Lda
    mov r3, #0xc0
ov006_02200770_Lda:
    ldr r0, =native_data_0220badc
    lsl r4, r5, #0x2
    ldrh r0, [r0, r4]
    add r2, sp, #0x8
    str r2, [sp]
    ldr r2, =native_data_0220baf4
    ldrh r2, [r2, r4]
    add r2, r0, r2
    bl native_fn_022038d8
    mov r0, #0x0
    add r1, r0, #0x0
    add r2, sp, #0x8
    bl native_fn_022039a4
    add sp, #0x10
    pop {r3, r4, r5, r6, r7, pc}
}
