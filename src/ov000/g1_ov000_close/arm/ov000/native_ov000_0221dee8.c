/* ov000 row 0x0221dee8: 340 bytes.
 *
 * What it does: 83 instructions; 5 call(s) to 0x02048a60, 0x02048a94, 0x0221dff4, +2 more; loops (back edge at +0x70); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x14c -> constant 0x02246318 (image word 0x02246318)
 *   pool +0x150 -> constant 0x02246348 (image word 0x02246348)
 *   branch +0x18 -> +0x124
 *   branch +0x28 -> +0x124
 *   branch +0x44 -> +0x98
 *   branch +0x94 -> +0xac
 *   branch +0xb4 -> +0x10c
 *   test +0x0c cmp r3, #2
 *   test +0x10 cmpne r3, #3
 *   test +0x14 cmpne r3, #8
 *   test +0x24 cmp r0, #0
 *   test +0x40 cmp r2, r0
 *   test +0x58 cmp r0, #1
 *   test +0xb0 cmp r0, #0
 *   test +0xd0 cmp r0, #1
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221dee8; the literal pool and
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

extern void native_fn_02048a60(void);
extern void native_fn_02048a94(void);


asm u32 native_ov000_0221dee8 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    ldrsb r3, [r4, #16]
    cmp r3, #2
    cmpne r3, #3
    cmpne r3, #8
    bne ov000_0221dee8_L124
    ldr r0, =0x02246318
    ldrb r0, [r0]
    cmp r0, #0
    bne ov000_0221dee8_L124
    ldrh r1, [r4, #14]
    ldrh r0, [r4, #12]
    ldr r2, [r4, #0x4]
    sub r0, r1, r0
    sub r0, r0, #1
    cmp r2, r0
    bgt ov000_0221dee8_L98
    sub r0, r3, #2
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    and r0, r0, #255
    cmp r0, #1
    ldr r0, =0x02246348
    movls r2, #144
    ldr r0, [r0, #0x30]
    mov r1, #240
    movhi r2, #136
    bl native_fn_02048a60
    ldr r0, =0x02246348
    mov r1, #1
    ldr r3, [r0, #0x30]
    ldr r2, [r3, #0x7c]
    orr r2, r2, #2
    str r2, [r3, #0x7c]
    ldr r0, [r0, #0x30]
    bl native_fn_02048a94
    b ov000_0221dee8_Lac
ov000_0221dee8_L98:
    ldr r0, =0x02246348
    ldr r1, [r0, #0x30]
    ldr r0, [r1, #0x7c]
    bic r0, r0, #2
    str r0, [r1, #0x7c]
ov000_0221dee8_Lac:
    ldr r0, [r4, #0x4]
    cmp r0, #0
    ble ov000_0221dee8_L10c
    ldrsb r0, [r4, #16]
    mov r1, #240
    sub r0, r0, #2
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    and r0, r0, #255
    cmp r0, #1
    ldr r0, =0x02246348
    movls r2, #40
    ldr r0, [r0, #0x2c]
    movhi r2, #48
    bl native_fn_02048a60
    ldr r0, =0x02246348
    mov r1, #1
    ldr r3, [r0, #0x2c]
    ldr r2, [r3, #0x7c]
    orr r2, r2, #2
    str r2, [r3, #0x7c]
    ldr r0, [r0, #0x2c]
    bl native_fn_02048a94
    ldmia sp!, {r4, pc}
ov000_0221dee8_L10c:
    ldr r0, =0x02246348
    ldr r1, [r0, #0x2c]
    ldr r0, [r1, #0x7c]
    bic r0, r0, #2
    str r0, [r1, #0x7c]
    ldmia sp!, {r4, pc}
ov000_0221dee8_L124:
    ldr r0, =0x02246348
    ldr r2, [r0, #0x30]
    ldr r1, [r2, #0x7c]
    bic r1, r1, #2
    str r1, [r2, #0x7c]
    ldr r1, [r0, #0x2c]
    ldr r0, [r1, #0x7c]
    bic r0, r0, #2
    str r0, [r1, #0x7c]
    ldmia sp!, {r4, pc}
}
