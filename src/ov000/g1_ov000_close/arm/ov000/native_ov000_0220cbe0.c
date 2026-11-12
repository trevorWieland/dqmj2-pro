/* ov000 row 0x0220cbe0: 328 bytes.
 *
 * What it does: 82 instructions; 15 call(s) to 0x020c56b4, 0x020c56b4, 0x020c56b4, +12 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x24 -> +0x13c
 *   branch +0xb0 -> +0x124
 *   back edge +0x120 -> +0xb8
 *   test +0x20 cmp r0, #0
 *   test +0xa8 cmp r9, #0
 *   test +0x118 cmp r6, r9
 *   test +0x130 cmp r7, r0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220cbe0; the literal pool and
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

extern void native_fn_020c56b4(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02062a50(void);
extern void native_fn_0207b460(void);
extern void native_fn_02210f74(void);
extern void native_fn_02210f84(void);
extern void native_fn_02002480(void);


asm u32 native_ov000_0220cbe0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #64
    add r0, r0, #512
    ldrsh r9, [r0, #118]
    mov r4, #0
    mov r0, r9
    bl native_fn_020c56b4
    ldrb r0, [r0, #0x9]
    cmp r0, #0
    beq ov000_0220cbe0_L13c
    mov r0, r9
    bl native_fn_020c56b4
    mov r6, r0
    mov r0, r9
    bl native_fn_020c56b4
    mov r5, r0
    mov r0, r9
    bl native_fn_020c56b4
    mov r4, r0
    mov r0, r9
    bl native_fn_020c56b4
    mov r8, r0
    mov r0, r9
    bl native_fn_020c56b4
    mov r7, r0
    mov r0, r9
    bl native_fn_020c56b4
    ldrh r2, [r8, #32]
    ldrh r1, [r7, #28]
    ldrh r0, [r0, #30]
    ldrh r3, [r4, #34]
    mov r8, #0
    add r0, r1, r0
    add r0, r2, r0
    ldrh r1, [r5, #36]
    add r0, r3, r0
    ldrh r2, [r6, #38]
    add r0, r1, r0
    add r0, r2, r0
    add r7, r0, r0, lsl #1
    bl native_fn_02062aa0
    mov r9, r0
    cmp r9, #0
    mov r6, r8
    ble ov000_0220cbe0_L124
    add r4, sp, #0
ov000_0220cbe0_Lb8:
    mov r0, r6
    bl native_fn_02062a50
    mov r5, r0
    ldrsh r0, [r5, #24]
    ldrb r1, [r5, #0x1a]
    mov r3, r4
    add r2, r5, #122
    bl native_fn_0207b460
    mov r0, r5
    mov r1, r4
    bl native_fn_02210f74
    add r8, r8, r0
    mov r0, r5
    mov r1, r4
    bl native_fn_02210f84
    add r3, r8, r0
    ldrsh r2, [r5, #40]
    ldrsh r1, [r5, #42]
    ldrsh r0, [r5, #44]
    add r2, r3, r2
    add r1, r2, r1
    add r1, r1, r0
    ldrsh r0, [r5, #46]
    add r6, r6, #1
    cmp r6, r9
    add r8, r1, r0
    blt ov000_0220cbe0_Lb8
ov000_0220cbe0_L124:
    mov r0, r8
    mov r1, r9
    bl native_fn_02002480
    cmp r7, r0
    movlt r4, #1
    movge r4, #0
ov000_0220cbe0_L13c:
    mov r0, r4
    add sp, sp, #64
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
