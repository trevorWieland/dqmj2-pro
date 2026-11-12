/* ov000 row 0x021f36f8: 376 bytes.
 *
 * What it does: 92 instructions; 9 call(s) to 0x02042d58, 0x0202859c, 0x0202859c, +6 more; loops (back edge at +0x34); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x170 -> constant 0x02236ed8 (image word 0x02236ed8)
 *   pool +0x174 -> constant 0x00000438 (image word 0x00000438)
 *   branch +0x3c -> +0x164
 *   branch +0x48 -> +0x158
 *   back edge +0x160 -> +0x28
 *   test +0x38 cmp r0, #0
 *   test +0x44 cmp r0, #5
 *   test +0x114 cmp r4, r9
 *   test +0x15c cmp r0, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f36f8; the literal pool and
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

extern void native_fn_02042d58(void);
extern void native_fn_0202859c(void);
extern void native_fn_0200235c(void);
extern void native_fn_021e7160(void);


asm u32 native_ov000_021f36f8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #8
    mov r10, r0
    ldr r1, [r10, #0x60]
    mov r0, #0
    ldr r1, [r1]
    ldr r11, =0x02236ed8
    str r0, [sp, #0x4]
    mov r0, r1, asr #12
    str r0, [sp]
ov000_021f36f8_L28:
    ldr r0, [r10, #0x164]
    ldr r1, [sp]
    add r2, sp, #4
    bl native_fn_02042d58
    cmp r0, #0
    beq ov000_021f36f8_L164
    ldrh r0, [r0, #2]
    cmp r0, #5
    bne ov000_021f36f8_L158
    ldr r1, [r11, #0x8]
    mov r0, #0
    smull r3, r2, r1, r1
    adds r3, r3, #2048
    mov r1, r0
    adc r1, r2, r1
    mov r9, r3, lsr #12
    orr r9, r9, r1, lsl #20
    mov r1, r0
    bl native_fn_0202859c
    mov r8, r0
    mov r0, #0
    mov r1, r0
    bl native_fn_0202859c
    mov r7, r0
    mov r0, #0
    mov r1, r0
    bl native_fn_0202859c
    mov r6, r0
    mov r0, #0
    mov r1, r0
    bl native_fn_0202859c
    mov r5, r0
    mov r0, #0
    mov r1, r0
    bl native_fn_0202859c
    mov r4, r0
    mov r0, #0
    mov r1, r0
    bl native_fn_0202859c
    ldr r3, [r7, #0x8]
    ldr r2, [r6]
    ldr r1, [r5]
    ldr r5, [r0, #0x4]
    ldr r0, [r10, #0x78]
    ldr r8, [r8, #0x8]
    ldr r6, [r4, #0x4]
    ldr r7, [r10, #0x70]
    sub r4, r0, r8
    sub r3, r0, r3
    sub r0, r7, r2
    sub r7, r7, r1
    ldr r1, [r10, #0x74]
    sub r2, r1, r6
    sub r1, r1, r5
    smull r5, r1, r2, r1
    smlal r5, r1, r0, r7
    smlal r5, r1, r4, r3
    mov r4, r5, lsr #12
    orr r4, r4, r1, lsl #20
    cmp r4, r9
    ldr r0, [r11]
    movge r4, r9
    smull r3, r2, r4, r0
    mov r0, #2048
    adds r3, r3, r0
    mov r0, #0
    adc r2, r2, r0
    mov r0, r3, lsr #12
    mov r1, r9
    orr r0, r0, r2, lsl #20
    bl native_fn_0200235c
    ldr r2, [r11]
    mov r1, #100
    sub r2, r2, r0
    ldr r0, =0x00000438
    bl native_fn_021e7160
ov000_021f36f8_L158:
    ldr r0, [sp, #0x4]
    cmp r0, #0
    bge ov000_021f36f8_L28
ov000_021f36f8_L164:
    mov r0, #0
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
