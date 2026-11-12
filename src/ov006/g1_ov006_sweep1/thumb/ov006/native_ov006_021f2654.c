/* ov006 row 0x021f2654: 144 bytes.
 *
 * What it does: Writes one block of 1 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x84 -> native_data5_0221c008 (image word 0x0221c008)
 *   pool +0x88 -> native_data_0220b0e8 (image word 0x0220b0e8)
 *   pool +0x8c -> native_data_0220b0cc (image word 0x0220b0cc)
 *   branch +0x16 -> +0x82
 *   branch +0x22 -> +0x5e
 *   back edge +0x5c -> +0x26
 *   branch +0x78 -> +0x82
 *   test +0x14 cmp r0, #0x10
 *   test +0x20 cmp r7, #0x0
 *   test +0x5a cmp r4, r7
 *   test +0x76 cmp r1, #0x0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f2654; the literal pool and
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

extern u8 native_data5_0221c008[];
extern u8 native_data_0220b0e8[];
extern u8 native_data_0220b0cc[];
extern void native_fn_02202dc0(void);
extern void native_fn_02202ff0(void);
extern void native_fn_02202f54(void);
extern void native_fn_021f2404(void);
extern void native_fn_02204974(void);


asm u32 native_ov006_021f2654 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    str r0, [sp]
    ldr r0, =native_data5_0221c008
    ldr r1, [r0, #0]
    ldrh r0, [r1, #0x14]
    add r0, r0, #0x1
    strh r0, [r1, #0x14]
    ldr r0, =native_data5_0221c008
    ldr r1, [r0, #0]
    ldrh r0, [r1, #0x14]
    cmp r0, #0x10
    blo ov006_021f2654_L82
    ldrb r1, [r1, #0x17]
    ldr r0, =native_data_0220b0e8
    mov r4, #0x0
    ldrb r7, [r0, r1]
    cmp r7, #0x0
    ble ov006_021f2654_L5e
    add r5, r4, #0x0
ov006_021f2654_L26:
    ldr r0, =native_data5_0221c008
    ldr r0, [r0, #0]
    ldrb r1, [r0, #0x17]
    ldr r0, [r0, r5]
    lsl r2, r1, #0x1
    ldr r1, =native_data_0220b0cc
    add r1, r1, r2
    ldrb r6, [r4, r1]
    mov r1, #0x0
    bl native_fn_02202dc0
    add r2, r0, #0x0
    mov r0, #0x0
    add r1, r6, #0x0
    bl native_fn_02202ff0
    ldr r0, =native_data5_0221c008
    mov r1, #0x0
    ldr r0, [r0, #0]
    mvn r1, r1
    ldr r0, [r0, r5]
    mov r2, #0x1
    bl native_fn_02202f54
    add r4, r4, #0x1
    add r5, r5, #0x4
    cmp r4, r7
    blt ov006_021f2654_L26
ov006_021f2654_L5e:
    mov r0, #0xa8
    bl native_fn_021f2404
    ldr r1, =native_data5_0221c008
    mov r0, #0x0
    ldr r2, [r1, #0]
    sub r3, r0, #0x1
    strh r0, [r2, #0x14]
    ldr r2, [r1, #0]
    strb r3, [r2, #0x16]
    ldr r2, [r1, #0]
    ldr r1, [r2, #0x10]
    cmp r1, #0x0
    beq ov006_021f2654_L82
    ldr r1, [sp]
    str r0, [r2, #0x10]
    bl native_fn_02204974
ov006_021f2654_L82:
    pop {r3, r4, r5, r6, r7, pc}
}
