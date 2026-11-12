/* ov000 row 0x021df950: 268 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (3 loads, 3 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x100 -> constant 0x02231bf0 (image word 0x02231bf0)
 *   pool +0x104 -> constant 0x02231f64 (image word 0x02231f64)
 *   pool +0x108 -> constant 0x02231f68 (image word 0x02231f68)
 *   branch +0x18 -> +0xf8
 *   branch +0x24 -> +0xf8
 *   branch +0x84 -> +0x8c
 *   back edge +0x94 -> +0x70
 *   branch +0xb4 -> +0xbc
 *   back edge +0xc4 -> +0xa0
 *   branch +0xe4 -> +0xec
 *   back edge +0xf4 -> +0xd0
 *   test +0x10 cmp r0, #0
 *   test +0x20 cmp r0, #0
 *   test +0x80 cmp r0, #0
 *   test +0x90 cmp r6, #4
 *   test +0xb0 cmp r0, #0
 *   test +0xc0 cmp r7, #4
 *   test +0xe0 cmp r0, #0
 *   test +0xf0 cmp r7, #4
 *   1 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021df950; the literal pool and
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

extern void native_fn_021df544(void);
extern void native_fn_021df578(void);
extern void native_fn_021df7f4(void);
extern void native_fn_021df868(void);
extern void native_fn_021df8dc(void);


asm u32 native_ov000_021df950 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r4, #0
    mov r6, r0
    bl native_fn_021df544
    cmp r0, #0
    movne r4, #1
    bne ov000_021df950_Lf8
    bl native_fn_021df578
    cmp r0, #0
    blt ov000_021df950_Lf8
    mov r1, #48
    mov r2, #44
    mul r14, r0, r1
    ldr r7, =0x02231bf0
    ldr r3, =0x02231f64
    mul r5, r6, r2
    ldr r0, [r7, #0x8]
    ldr r1, =0x02231f68
    str r6, [r3, lr]
    add r12, r0, r5
    add r6, r1, lr
    ldmia r12!, {r0, r1, r2, r3}
    stmia r6!, {r0, r1, r2, r3}
    ldmia r12!, {r0, r1, r2, r3}
    stmia r6!, {r0, r1, r2, r3}
    ldmia r12, {r0, r1, r2}
    stmia r6, {r0, r1, r2}
    mov r6, r4
ov000_021df950_L70:
    ldr r0, [r7, #0x8]
    add r0, r5, r0
    add r0, r0, r6, lsl #1
    ldrh r0, [r0, #16]
    cmp r0, #0
    beq ov000_021df950_L8c
    bl native_fn_021df7f4
ov000_021df950_L8c:
    add r6, r6, #1
    cmp r6, #4
    blt ov000_021df950_L70
    ldr r6, =0x02231bf0
    mov r7, #0
ov000_021df950_La0:
    ldr r0, [r6, #0x8]
    add r0, r5, r0
    add r0, r0, r7, lsl #1
    ldrh r0, [r0, #24]
    cmp r0, #0
    beq ov000_021df950_Lbc
    bl native_fn_021df868
ov000_021df950_Lbc:
    add r7, r7, #1
    cmp r7, #4
    blt ov000_021df950_La0
    ldr r6, =0x02231bf0
    mov r7, #0
ov000_021df950_Ld0:
    ldr r0, [r6, #0x8]
    add r0, r5, r0
    add r0, r0, r7, lsl #1
    ldrh r0, [r0, #32]
    cmp r0, #0
    beq ov000_021df950_Lec
    bl native_fn_021df8dc
ov000_021df950_Lec:
    add r7, r7, #1
    cmp r7, #4
    blt ov000_021df950_Ld0
ov000_021df950_Lf8:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
