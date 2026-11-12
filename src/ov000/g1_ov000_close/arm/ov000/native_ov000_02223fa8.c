/* ov000 row 0x02223fa8: 184 bytes.
 *
 * What it does: 45 instructions; 9 call(s) to 0x01ffb4ec, 0x01ffa8f0, 0x01ffb4ec, +6 more; loops (back edge at +0x1c); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xb4 -> native_data_0222fdd8 (image word 0x0222fdd8)
 *   branch +0x38 -> +0x90
 *   branch +0x60 -> +0x84
 *   branch +0x70 -> +0x84
 *   back edge +0x8c -> +0x3c
 *   back edge +0x98 -> +0x18
 *   test +0x34 cmp r8, r10
 *   test +0x5c cmp r2, r1
 *   test +0x6c cmp r1, r0
 *   test +0x88 cmp r8, r10
 *   test +0x94 cmp r7, #8
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02223fa8; the literal pool and
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

extern u8 native_data_0222fdd8[];
extern void native_fn_01ffb4ec(void);
extern void native_fn_01ffa8f0(void);
extern void native_fn_01ffa824(void);
extern void native_fn_01ffa8a8(void);


asm u32 native_ov000_02223fa8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    ldr r2, =native_data_0222fdd8
    mov r1, r0, lsl #3
    ldrsb r9, [r2, r1]
    add r6, r2, r0, lsl #3
    mov r7, #0
ov000_02223fa8_L18:
    and r0, r7, #255
    bl native_fn_01ffb4ec
    mov r5, r0
    add r4, r5, #256
    ldrsb r0, [r4, #101]
    ldrsb r8, [r6, r0]
    add r10, r8, r9
    cmp r8, r10
    bge ov000_02223fa8_L90
ov000_02223fa8_L3c:
    mov r0, r8, lsl #24
    mov r0, r0, asr #24
    bl native_fn_01ffa8f0
    and r0, r0, #255
    bl native_fn_01ffb4ec
    add r1, r0, #256
    ldrsb r2, [r4, #101]
    ldrsb r1, [r1, #101]
    cmp r2, r1
    beq ov000_02223fa8_L84
    ldrb r1, [r5, #0x166]
    ldrb r0, [r0, #0x166]
    cmp r1, r0
    bne ov000_02223fa8_L84
    mov r0, r8, lsl #24
    mov r0, r0, asr #24
    bl native_fn_01ffa8f0
    strb r0, [r5, #0x164]
ov000_02223fa8_L84:
    add r8, r8, #1
    cmp r8, r10
    blt ov000_02223fa8_L3c
ov000_02223fa8_L90:
    add r7, r7, #1
    cmp r7, #8
    blt ov000_02223fa8_L18
    bl native_fn_01ffa824
    and r0, r0, #255
    bl native_fn_01ffb4ec
    ldrb r0, [r0, #0x164]
    bl native_fn_01ffa8a8
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
