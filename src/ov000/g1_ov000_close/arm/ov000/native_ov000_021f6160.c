/* ov000 row 0x021f6160: 232 bytes.
 *
 * What it does: 57 instructions; 9 call(s) to 0x02061944, 0x01ffa824, 0x01ffb4ec, +6 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xe4 -> constant 0x02236ee4 (image word 0x02236ee4)
 *   branch +0x2c -> +0xd4
 *   branch +0x40 -> +0xb0
 *   branch +0x70 -> +0x80
 *   branch +0xbc -> +0xd8
 *   back edge +0xcc -> +0xc4
 *   branch +0xd0 -> +0xd8
 *   test +0x18 cmp r0, #42
 *   test +0x28 cmp r1, #0
 *   test +0x3c cmp r1, #1
 *   test +0x5c cmp r0, #4
 *   test +0xb8 cmp r0, #0
 *   test +0xc8 cmp r0, #0
 *   1 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f6160; the literal pool and
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

extern void native_fn_02061944(void);
extern void native_fn_01ffa824(void);
extern void native_fn_01ffb4ec(void);
extern void native_fn_021f5eb0(void);
extern void native_fn_01ffa8d8(void);
extern void native_fn_0204aeb4(void);
extern void native_fn_021f5cdc(void);
extern void native_fn_021f6294(void);


asm u32 native_ov000_021f6160 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #16
    bl native_fn_02061944
    add r0, r0, #512
    ldrsb r0, [r0, #108]
    mov r4, #0
    cmp r0, #42
    ldr r0, =0x02236ee4
    movne r4, #1
    ldrb r1, [r0, #0x2]
    cmp r1, #0
    beq ov000_021f6160_Ld4
    sub r2, r1, #1
    and r1, r2, #255
    strb r2, [r0, #0x2]
    cmp r1, #1
    bne ov000_021f6160_Lb0
    bl native_fn_01ffa824
    and r0, r0, #255
    bl native_fn_01ffb4ec
    mov r5, r0
    bl native_fn_021f5eb0
    bl native_fn_01ffa8d8
    cmp r0, #4
    add r0, r5, #256
    ldrnesb r0, [r0, #101]
    movne r0, r0, lsl #1
    addne r0, r0, #5
    bne ov000_021f6160_L80
    ldrsb r0, [r0, #101]
    mov r0, r0, lsl #2
    add r0, r0, #7
ov000_021f6160_L80:
    mov r0, r0, lsl #24
    mov r1, #0
    mov r2, r0, asr #24
    str r1, [sp]
    mov r0, #1
    stmib sp, {r0, r2}
    ldr r0, =0x02236ee4
    str r1, [sp, #0xc]
    ldr r0, [r0, #0x1c]
    mov r2, r1
    mov r3, #15
    bl native_fn_0204aeb4
ov000_021f6160_Lb0:
    ldr r0, =0x02236ee4
    ldrb r0, [r0, #0x2]
    cmp r0, #0
    bne ov000_021f6160_Ld8
    bl native_fn_021f5cdc
ov000_021f6160_Lc4:
    bl native_fn_021f6294
    cmp r0, #0
    beq ov000_021f6160_Lc4
    b ov000_021f6160_Ld8
ov000_021f6160_Ld4:
    bl native_fn_021f6294
ov000_021f6160_Ld8:
    mov r0, r4
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, pc}
}
