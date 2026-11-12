/* main row 0x0204d258: 500 bytes.
 *
 * What it does: Writes one block of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x1f0 -> constant 0x45800000 (image word 0x45800000)
 *   branch +0x64 -> +0x80
 *   branch +0x7c -> +0x90
 *   branch +0xa4 -> +0xbc
 *   branch +0xb8 -> +0xc8
 *   branch +0xe0 -> +0xf8
 *   branch +0xf4 -> +0x104
 *   branch +0x11c -> +0x134
 *   branch +0x130 -> +0x140
 *   15 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0204d258; the literal pool and
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

extern void native_fn_020259b4(void);
extern void native_fn_020259e8(void);
extern void native_fn_0202537c(void);
extern void native_fn_02025ab8(void);
extern void native_fn_02024e0c(void);
extern void native_fn_02025ca4(void);
extern void native_fn_02209dac(void);
extern void native_fn_0220a358(void);
extern void native_fn_02025a28(void);


asm u32 native_main_0204d258 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #28
    mov r10, r0
    ldr r0, [r10, #0x10]
    mov r11, r1
    bl native_fn_020259b4
    str r0, [sp, #0x18]
    ldr r0, [r10, #0x24]
    ldr r6, [r10, #0x14]
    ldr r7, [r10, #0x18]
    ldr r8, [r10, #0x1c]
    ldr r9, [r10, #0x20]
    bl native_fn_020259b4
    str r0, [sp, #0x14]
    ldr r0, [r10, #0x28]
    bl native_fn_020259e8
    and r4, r0, #255
    ldr r0, [r10, #0x2c]
    bl native_fn_020259e8
    and r5, r0, #255
    mov r0, r9
    mov r1, #0
    bl native_fn_0202537c
    ldr r0, =0x45800000
    mov r1, r9
    bls main_0204d258_L80
    bl native_fn_02025ab8
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    str r0, [sp, #0x10]
    b main_0204d258_L90
main_0204d258_L80:
    bl native_fn_02025ab8
    mov r1, #1056964608
    bl native_fn_02025ca4
    str r0, [sp, #0x10]
main_0204d258_L90:
    mov r0, r8
    mov r1, #0
    bl native_fn_0202537c
    ldr r0, =0x45800000
    mov r1, r8
    bls main_0204d258_Lbc
    bl native_fn_02025ab8
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b main_0204d258_Lc8
main_0204d258_Lbc:
    bl native_fn_02025ab8
    mov r1, #1056964608
    bl native_fn_02025ca4
main_0204d258_Lc8:
    mov r8, r0
    mov r0, r7
    mov r1, #0
    bl native_fn_0202537c
    ldr r0, =0x45800000
    mov r1, r7
    bls main_0204d258_Lf8
    bl native_fn_02025ab8
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b main_0204d258_L104
main_0204d258_Lf8:
    bl native_fn_02025ab8
    mov r1, #1056964608
    bl native_fn_02025ca4
main_0204d258_L104:
    mov r7, r0
    mov r0, r6
    mov r1, #0
    bl native_fn_0202537c
    ldr r0, =0x45800000
    mov r1, r6
    bls main_0204d258_L134
    bl native_fn_02025ab8
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b main_0204d258_L140
main_0204d258_L134:
    bl native_fn_02025ab8
    mov r1, #1056964608
    bl native_fn_02025ca4
main_0204d258_L140:
    bl native_fn_020259b4
    mov r6, r0
    mov r0, r7
    bl native_fn_020259b4
    mov r7, r0
    mov r0, r8
    bl native_fn_020259b4
    mov r8, r0
    ldr r0, [sp, #0x10]
    bl native_fn_020259b4
    str r0, [sp]
    ldr r0, [sp, #0x14]
    mov r1, r6
    stmib sp, {r0, r4, r5}
    ldr r0, [sp, #0x18]
    mov r2, r7
    mov r3, r8
    bl native_fn_02209dac
    mov r4, r0
    bl native_fn_0220a358
    mov r0, r4
    bl native_fn_02025a28
    str r0, [r10, #0x10]
    mov r5, #0
    str r5, [r10, #0x14]
    str r5, [r10, #0x18]
    str r5, [r10, #0x1c]
    str r5, [r10, #0x20]
    str r5, [r10, #0x24]
    str r5, [r10, #0x28]
    str r5, [r10, #0x2c]
    ldrb r2, [r10, #0x3]
    mov r0, #268
    add r4, r10, #1136
    mul r3, r2, r0
    ldr r1, [r11, #0x4]
    ldr r2, [r4, r3]
    add r1, r2, r1
    str r1, [r4, r3]
    ldrb r1, [r10, #0x3]
    mla r0, r1, r0, r10
    strb r5, [r0, #0x477]
    add sp, sp, #28
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
