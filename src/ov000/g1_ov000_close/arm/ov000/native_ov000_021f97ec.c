/* ov000 row 0x021f97ec: 172 bytes.
 *
 * What it does: 43 instructions; 4 call(s) to 0x02215698, 0x02066c3c, 0x0206d250, +1 more; loops (back edge at +0x10); returns through pop {r3, r4, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x2c -> +0x38
 *   branch +0x54 -> +0x60
 *   test +0x24 cmp r1, #216
 *   test +0x30 cmp r2, #0
 *   test +0x4c cmp r0, #152
 *   test +0x58 cmp r1, #0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f97ec; the literal pool and
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

extern void ov000_display_context_02215698(void);
extern void native_fn_02066c3c(void);
extern void native_fn_0206d250(void);
extern void native_fn_021f9558(void);


asm u32 native_ov000_021f97ec (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #4
    bl ov000_display_context_02215698
    mov r4, r0
    bl native_fn_02066c3c
    ldrb r1, [r0, #0x1]
    subs r2, r1, #20
    movmi r1, #0
    movpl r1, r2
    cmp r1, #216
    movgt r2, #216
    bgt ov000_021f97ec_L38
    cmp r2, #0
    movlt r2, #0
ov000_021f97ec_L38:
    strb r2, [r4, #0x498]
    ldrb r0, [r0, #0x2]
    subs r1, r0, #20
    movmi r0, #0
    movpl r0, r1
    cmp r0, #152
    movgt r1, #152
    bgt ov000_021f97ec_L60
    cmp r1, #0
    movlt r1, #0
ov000_021f97ec_L60:
    strb r1, [r4, #0x499]
    ldrb r1, [r4, #0x498]
    add r0, r4, #1024
    strh r1, [sp]
    ldrb r1, [r4, #0x499]
    strh r1, [sp, #2]
    ldrsb r0, [r0, #151]
    add r0, r4, r0, lsl #3
    ldrsb r0, [r0, #166]
    bl native_fn_0206d250
    mov r1, r0
    add r0, sp, #0
    bl native_fn_021f9558
    ldrsh r0, [sp]
    strb r0, [r4, #0x498]
    ldrsh r0, [sp, #2]
    strb r0, [r4, #0x499]
    add sp, sp, #4
    ldmia sp!, {r3, r4, pc}
}
