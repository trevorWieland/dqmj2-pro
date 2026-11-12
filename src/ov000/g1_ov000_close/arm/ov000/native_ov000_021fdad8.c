/* ov000 row 0x021fdad8: 172 bytes.
 *
 * What it does: 42 instructions; 8 call(s) to 0x021fdb78, 0x02062d04, 0x021fdb64, +5 more; loops (back edge at +0x38); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xa8 -> constant 0x022372a8 (image word 0x022372a8)
 *   branch +0x28 -> +0xa0
 *   branch +0x40 -> +0x8c
 *   branch +0x48 -> +0x8c
 *   branch +0x64 -> +0x8c
 *   back edge +0x9c -> +0x2c
 *   test +0x24 cmp r0, #0
 *   test +0x3c cmp r0, #0
 *   test +0x44 cmp r5, #0
 *   test +0x60 cmp r0, #0
 *   test +0x84 cmp r1, r0
 *   test +0x98 cmp r4, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fdad8; the literal pool and
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

extern void native_fn_02062d04(void);
extern void native_fn_02065d88(void);
extern void native_fn_02211064(void);


asm u32 native_ov000_021fdad8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    movs r7, r0
    moveq r0, #0
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
    ldr r8, =0x022372a8
    ldrb r6, [r7, #0x31]
    ldr r1, [r8, #0xc]
    mov r4, #0
    ldr r0, [r1, #0x5f0]
    cmp r0, #0
    ble ov000_021fdad8_La0
ov000_021fdad8_L2c:
    add r0, r1, r4, lsl #2
    ldr r5, [r0, #0x1f0]
    mov r0, r5
    bl native_fn_02062d04
    cmp r0, #0
    ble ov000_021fdad8_L8c
    cmp r5, #0
    beq ov000_021fdad8_L8c
    mov r0, r5
    bl native_fn_02065d88
    ldrb r1, [r0, #0x2d]
    mov r0, r7
    bl native_fn_02211064
    cmp r0, #0
    beq ov000_021fdad8_L8c
    mov r0, r5
    bl native_fn_02065d88
    mov r9, r0
    mov r0, r6
    bl native_fn_02065d88
    ldrh r1, [r9, #28]
    ldrh r0, [r0, #28]
    cmp r1, r0
    movhi r6, r5
ov000_021fdad8_L8c:
    ldr r1, [r8, #0xc]
    add r4, r4, #1
    ldr r0, [r1, #0x5f0]
    cmp r4, r0
    blt ov000_021fdad8_L2c
ov000_021fdad8_La0:
    mov r0, r6
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
