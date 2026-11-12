/* ov006 row 0x021f37f0: 404 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x178 -> native_data_0220b168 (image word 0x0220b168)
 *   pool +0x17c -> native_data_0220b1b4 (image word 0x0220b1b4)
 *   pool +0x180 -> native_data_0221c05c (image word 0x0221c05c)
 *   pool +0x184 -> constant 0xc1fffcff (image word 0xc1fffcff)
 *   pool +0x188 -> constant 0xfe00ff00 (image word 0xfe00ff00)
 *   pool +0x18c -> native_data_0220b18c (image word 0x0220b18c)
 *   pool +0x190 -> native_data_0220b184 (image word 0x0220b184)
 *   branch +0x5a -> +0xa8
 *   back edge +0xa6 -> +0x6c
 *   branch +0xaa -> +0xd4
 *   branch +0xe6 -> +0x12c
 *   back edge +0x12a -> +0xf8
 *   branch +0x134 -> +0x174
 *   back edge +0x172 -> +0x13a
 *   test +0x58 cmp r0, #0x0
 *   test +0xa4 cmp r1, r0
 *   test +0xa8 cmp r7, #0x4
 *   test +0xe4 cmp r1, #0x0
 *   test +0x128 cmp r2, r3
 *   test +0x132 cmp r0, #0x0
 *   test +0x170 cmp r5, r0
 *   23 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f37f0; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220b168[];
extern u8 native_data2_0220b1b4[];
extern u8 native_data7_0221c05c[];
extern void native_fn_02203848(void);
extern void native_fn_020024bc(void);
extern u8 native_data_0220b18c[];
extern u8 native_data_0220b184[];
extern void native_fn_02202dcc(void);
extern void native_fn_02202eb0(void);


asm u32 native_ov006_021f37f0 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x20
    add r7, r1, #0x0
    ldr r1, =native_data_0220b168
    str r2, [sp, #0x8]
    ldrb r2, [r1, #0x11]
    str r0, [sp, #0x4]
    add r0, sp, #0x10
    strb r2, [r0, #0xa]
    ldrb r2, [r1, #0x12]
    strb r2, [r0, #0xb]
    ldrb r2, [r1, #0x13]
    strb r2, [r0, #0xc]
    ldrb r2, [r1, #0x14]
    strb r2, [r0, #0xd]
    ldrb r2, [r1, #0x15]
    strb r2, [r0, #0xe]
    ldrb r2, [r1, #0x16]
    strb r2, [r0, #0x5]
    ldrb r2, [r1, #0x17]
    strb r2, [r0, #0x6]
    ldrb r2, [r1, #0x18]
    strb r2, [r0, #0x7]
    ldrb r2, [r1, #0x19]
    strb r2, [r0, #0x8]
    ldrb r2, [r1, #0x1a]
    strb r2, [r0, #0x9]
    ldrb r2, [r1, #0xc]
    strb r2, [r0, #0]
    ldrb r2, [r1, #0xd]
    strb r2, [r0, #0x1]
    ldrb r2, [r1, #0xe]
    strb r2, [r0, #0x2]
    ldrb r2, [r1, #0xf]
    strb r2, [r0, #0x3]
    ldrb r1, [r1, #0x10]
    strb r1, [r0, #0x4]
    mov r0, #0xc
    mul r0, r7
    mov r12, r0
    add r0, sp, #0x18
    add r0, #0x2
    ldrb r0, [r0, r7]
    mov r1, #0x0
    cmp r0, #0x0
    ble ov006_021f37f0_La8
    mov r0, r12
    lsl r2, r0, #0x2
    ldr r0, =native_data2_0220b1b4
    add r3, r0, r2
    ldr r0, [sp, #0x8]
    lsl r0, r0, #0x18
    lsr r0, r0, #0x18
    str r0, [sp, #0xc]
ov006_021f37f0_L6c:
    ldr r0, =native_data7_0221c05c
    add r1, r1, #0x1
    ldr r0, [r0, #0]
    add r0, r0, r2
    ldr r5, [r0, #0x30]
    ldr r0, =0xc1fffcff
    ldr r4, [r5, #0]
    and r0, r4
    str r0, [r5, #0]
    ldr r0, =native_data7_0221c05c
    ldrh r4, [r3, #0]
    ldr r0, [r0, #0]
    add r3, r3, #0x4
    add r0, r0, r2
    ldr r0, [r0, #0x30]
    lsl r4, r4, #0x17
    lsr r6, r4, #0x7
    ldr r5, [r0, #0]
    ldr r4, =0xfe00ff00
    add r2, r2, #0x4
    and r5, r4
    ldr r4, [sp, #0xc]
    orr r4, r5
    orr r4, r6
    str r4, [r0, #0]
    add r0, sp, #0x18
    add r0, #0x2
    ldrb r0, [r0, r7]
    cmp r1, r0
    blt ov006_021f37f0_L6c
ov006_021f37f0_La8:
    cmp r7, #0x4
    bge ov006_021f37f0_Ld4
    ldr r0, =native_data7_0221c05c
    mov r1, r12
    ldr r3, [r0, #0]
    mov r0, #0x2
    str r0, [sp, #0]
    ldr r0, [sp, #0x4]
    lsl r2, r1, #0x2
    lsl r0, r0, #0x4
    ldr r1, =native_data2_0220b1b4
    lsl r4, r7, #0x2
    add r0, r3, r0
    ldr r0, [r4, r0]
    add r4, r3, r4
    mov r3, #0x41
    ldrh r1, [r1, r2]
    lsl r3, r3, #0x2
    ldr r2, [sp, #0x8]
    ldr r3, [r4, r3]
    bl native_fn_02203848
ov006_021f37f0_Ld4:
    add r0, r7, #0x3
    mov r1, #0x4
    blx native_fn_020024bc
    add r1, sp, #0x14
    add r1, #0x1
    ldrb r1, [r1, r7]
    mov r2, #0x0
    cmp r1, #0x0
    ble ov006_021f37f0_L12c
    ldr r1, [sp, #0x8]
    lsl r0, r0, #0x2
    lsl r1, r1, #0x18
    lsr r6, r1, #0x18
    ldr r1, =native_data_0220b18c
    ldrh r1, [r1, r0]
    lsl r1, r1, #0x17
    lsr r1, r1, #0x7
ov006_021f37f0_Lf8:
    ldr r3, =native_data7_0221c05c
    add r2, r2, #0x1
    ldr r3, [r3, #0]
    add r3, r0, r3
    add r3, #0xec
    ldr r5, [r3, #0]
    ldr r3, =0xc1fffcff
    ldr r4, [r5, #0]
    and r3, r4
    str r3, [r5, #0]
    ldr r3, =native_data7_0221c05c
    ldr r3, [r3, #0]
    add r3, r0, r3
    add r3, #0xec
    ldr r5, [r3, #0]
    ldr r3, =0xfe00ff00
    ldr r4, [r5, #0]
    and r3, r4
    orr r3, r6
    orr r3, r1
    str r3, [r5, #0]
    add r3, sp, #0x14
    add r3, #0x1
    ldrb r3, [r3, r7]
    cmp r2, r3
    blt ov006_021f37f0_Lf8
ov006_021f37f0_L12c:
    add r0, sp, #0x10
    ldrb r0, [r0, r7]
    mov r5, #0x0
    cmp r0, #0x0
    ble ov006_021f37f0_L174
    ldr r6, =native_data_0220b184
    add r4, r5, #0x0
ov006_021f37f0_L13a:
    ldr r0, =native_data7_0221c05c
    mov r1, #0x0
    ldr r0, [r0, #0]
    mov r2, #0x0
    add r0, r0, r4
    add r0, #0xfc
    ldr r0, [r0, #0]
    mvn r1, r1
    add r3, r2, #0x0
    bl native_fn_02202dcc
    ldr r0, =native_data7_0221c05c
    mov r1, #0x0
    ldr r0, [r0, #0]
    ldrh r2, [r6, #0]
    add r0, r0, r4
    add r0, #0xfc
    ldr r0, [r0, #0]
    ldr r3, [sp, #0x8]
    mvn r1, r1
    bl native_fn_02202eb0
    add r0, sp, #0x10
    ldrb r0, [r0, r7]
    add r5, r5, #0x1
    add r4, r4, #0x4
    add r6, r6, #0x4
    cmp r5, r0
    blt ov006_021f37f0_L13a
ov006_021f37f0_L174:
    add sp, #0x20
    pop {r3, r4, r5, r6, r7, pc}
}
