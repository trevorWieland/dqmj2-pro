/* ov006 row 0x021f4944: 384 bytes.
 *
 * What it does: Writes one block of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x164 -> native_data_0220b430 (image word 0x0220b430)
 *   pool +0x168 -> native_data_0220b482 (image word 0x0220b482)
 *   pool +0x16c -> native_data_0221c060 (image word 0x0221c060)
 *   pool +0x170 -> constant 0xc1fffcff (image word 0xc1fffcff)
 *   pool +0x174 -> constant 0xfe00ff00 (image word 0xfe00ff00)
 *   pool +0x178 -> native_data_0220b458 (image word 0x0220b458)
 *   pool +0x17c -> native_data_0220b460 (image word 0x0220b460)
 *   branch +0x58 -> +0xa6
 *   back edge +0xa4 -> +0x6a
 *   branch +0xa8 -> +0xc8
 *   branch +0xd2 -> +0x11c
 *   back edge +0x11a -> +0xe0
 *   branch +0x124 -> +0x160
 *   back edge +0x15e -> +0x12a
 *   test +0x56 cmp r0, #0x0
 *   test +0xa2 cmp r1, r0
 *   test +0xa6 cmp r7, #0x4
 *   test +0xd0 cmp r0, #0x0
 *   test +0x118 cmp r4, r0
 *   test +0x122 cmp r0, #0x0
 *   test +0x15c cmp r5, r0
 *   23 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f4944; the literal pool and
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

extern u8 native_data_0220b430[];
extern u8 native_data2_0220b482[];
extern u8 native_data7_0221c060[];
extern void native_fn_02203848(void);
extern u8 native_data_0220b458[];
extern u8 native_data_0220b460[];
extern void native_fn_02202dcc(void);
extern void native_fn_02202eb0(void);


asm u32 native_ov006_021f4944 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x20
    str r1, [sp, #0x4]
    ldr r1, =native_data_0220b430
    add r7, r0, #0x0
    ldrb r2, [r1, #0x15]
    add r0, sp, #0x10
    strb r2, [r0, #0xa]
    ldrb r2, [r1, #0x16]
    strb r2, [r0, #0xb]
    ldrb r2, [r1, #0x17]
    strb r2, [r0, #0xc]
    ldrb r2, [r1, #0x18]
    strb r2, [r0, #0xd]
    ldrb r2, [r1, #0x19]
    strb r2, [r0, #0xe]
    ldrb r2, [r1, #0x1a]
    strb r2, [r0, #0x5]
    ldrb r2, [r1, #0x1b]
    strb r2, [r0, #0x6]
    ldrb r2, [r1, #0x1c]
    strb r2, [r0, #0x7]
    ldrb r2, [r1, #0x1d]
    strb r2, [r0, #0x8]
    ldrb r2, [r1, #0x1e]
    strb r2, [r0, #0x9]
    ldrb r2, [r1, #0x10]
    strb r2, [r0, #0]
    ldrb r2, [r1, #0x11]
    strb r2, [r0, #0x1]
    ldrb r2, [r1, #0x12]
    strb r2, [r0, #0x2]
    ldrb r2, [r1, #0x13]
    strb r2, [r0, #0x3]
    ldrb r1, [r1, #0x14]
    strb r1, [r0, #0x4]
    lsl r0, r7, #0x1
    add r0, r7, r0
    mov r12, r0
    add r0, sp, #0x18
    add r0, #0x2
    ldrb r0, [r0, r7]
    mov r1, #0x0
    cmp r0, #0x0
    ble ov006_021f4944_La6
    mov r0, r12
    lsl r2, r0, #0x2
    ldr r0, =native_data2_0220b482
    add r3, r0, r2
    ldr r0, [sp, #0x4]
    lsl r0, r0, #0x18
    lsr r0, r0, #0x18
    str r0, [sp, #0x8]
ov006_021f4944_L6a:
    ldr r0, =native_data7_0221c060
    add r1, r1, #0x1
    ldr r0, [r0, #0]
    add r0, r0, r2
    ldr r5, [r0, #0x10]
    ldr r0, =0xc1fffcff
    ldr r4, [r5, #0]
    and r0, r4
    str r0, [r5, #0]
    ldr r0, =native_data7_0221c060
    ldrh r4, [r3, #0]
    ldr r0, [r0, #0]
    add r3, r3, #0x4
    add r0, r0, r2
    ldr r0, [r0, #0x10]
    lsl r4, r4, #0x17
    lsr r6, r4, #0x7
    ldr r5, [r0, #0]
    ldr r4, =0xfe00ff00
    add r2, r2, #0x4
    and r5, r4
    ldr r4, [sp, #0x8]
    orr r4, r5
    orr r4, r6
    str r4, [r0, #0]
    add r0, sp, #0x18
    add r0, #0x2
    ldrb r0, [r0, r7]
    cmp r1, r0
    blt ov006_021f4944_L6a
ov006_021f4944_La6:
    cmp r7, #0x4
    bge ov006_021f4944_Lc8
    ldr r0, =native_data7_0221c060
    mov r1, r12
    ldr r3, [r0, #0]
    mov r0, #0x2
    lsl r2, r1, #0x2
    ldr r1, =native_data2_0220b482
    str r0, [sp, #0]
    lsl r4, r7, #0x2
    ldr r0, [r3, r4]
    ldrh r1, [r1, r2]
    add r3, r3, r4
    ldr r2, [sp, #0x4]
    ldr r3, [r3, #0x48]
    bl native_fn_02203848
ov006_021f4944_Lc8:
    add r0, sp, #0x14
    add r0, #0x1
    ldrb r0, [r0, r7]
    mov r4, #0x0
    cmp r0, #0x0
    ble ov006_021f4944_L11c
    ldr r0, [sp, #0x4]
    ldr r3, =native_data_0220b458
    lsl r0, r0, #0x18
    lsr r0, r0, #0x18
    add r2, r4, #0x0
    str r0, [sp, #0xc]
ov006_021f4944_Le0:
    ldr r0, =native_data7_0221c060
    ldr r1, =0xc1fffcff
    ldr r0, [r0, #0]
    add r4, r4, #0x1
    add r0, r0, r2
    ldr r0, [r0, #0x38]
    ldr r5, [r0, #0]
    and r1, r5
    str r1, [r0, #0]
    ldr r0, =native_data7_0221c060
    ldr r5, =0xfe00ff00
    ldr r0, [r0, #0]
    add r0, r0, r2
    ldr r1, [r0, #0x38]
    ldrh r0, [r3, #0]
    ldr r6, [r1, #0]
    add r2, r2, #0x4
    and r6, r5
    ldr r5, [sp, #0xc]
    lsl r0, r0, #0x17
    lsr r0, r0, #0x7
    orr r5, r6
    orr r0, r5
    str r0, [r1, #0]
    add r0, sp, #0x14
    add r0, #0x1
    ldrb r0, [r0, r7]
    add r3, r3, #0x4
    cmp r4, r0
    blt ov006_021f4944_Le0
ov006_021f4944_L11c:
    add r0, sp, #0x10
    ldrb r0, [r0, r7]
    mov r5, #0x0
    cmp r0, #0x0
    ble ov006_021f4944_L160
    ldr r6, =native_data_0220b460
    add r4, r5, #0x0
ov006_021f4944_L12a:
    ldr r0, =native_data7_0221c060
    mov r1, #0x0
    ldr r0, [r0, #0]
    mov r2, #0x0
    add r0, r0, r4
    ldr r0, [r0, #0x40]
    mvn r1, r1
    add r3, r2, #0x0
    bl native_fn_02202dcc
    ldr r0, =native_data7_0221c060
    mov r1, #0x0
    ldr r0, [r0, #0]
    ldrh r2, [r6, #0]
    add r0, r0, r4
    ldr r0, [r0, #0x40]
    ldr r3, [sp, #0x4]
    mvn r1, r1
    bl native_fn_02202eb0
    add r0, sp, #0x10
    ldrb r0, [r0, r7]
    add r5, r5, #0x1
    add r4, r4, #0x4
    add r6, r6, #0x4
    cmp r5, r0
    blt ov006_021f4944_L12a
ov006_021f4944_L160:
    add sp, #0x20
    pop {r3, r4, r5, r6, r7, pc}
}
