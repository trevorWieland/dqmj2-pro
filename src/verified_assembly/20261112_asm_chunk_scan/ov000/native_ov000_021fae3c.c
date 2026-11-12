/* ov000 row 0x021fae3c: 452 bytes.
 *
 * What it does: Writes 4 blocks of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x1c0 -> constant 0x0223716c (image word 0x0223716c)
 *   back edge +0x30 -> +0x24
 *   branch +0x54 -> +0x1b4
 *   branch +0x8c -> +0xc4
 *   branch +0x98 -> +0x1b4
 *   branch +0xc0 -> +0xcc
 *   branch +0xd4 -> +0x168
 *   branch +0xd8 -> +0xf0
 *   branch +0xdc -> +0x104
 *   branch +0xe0 -> +0x140
 *   branch +0xe4 -> +0x168
 *   branch +0xe8 -> +0x168
 *   branch +0xec -> +0x168
 *   branch +0x100 -> +0x16c
 *   branch +0x13c -> +0x16c
 *   branch +0x164 -> +0x16c
 *   branch +0x170 -> +0x1a8
 *   branch +0x17c -> +0x190
 *   branch +0x180 -> +0x19c
 *   branch +0x18c -> +0x19c
 *   back edge +0x1b0 -> +0x7c
 *   test +0x50 cmp r0, #255
 *   test +0x88 cmp r6, #0
 *   test +0x94 cmp r8, r0
 *   test +0xcc cmp r7, #5
 *   test +0x16c cmp r6, #0
 *   test +0x178 cmp r10, r1
 *   test +0x188 cmp r11, r0
 *   test +0x1ac cmp r0, #0
 *   8 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fae3c; the literal pool and
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

extern void native_fn_021fbc9c(void);
extern void native_fn_021fb7e8(void);
extern void native_fn_021fb310(void);
extern void native_fn_021fadec(void);


asm u32 native_ov000_021fae3c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #332
    mov r0, #0
    str r0, [sp]
    add r5, sp, #20
    mov r1, r0
    mov r2, r0
    mov r3, r0
    mov r4, #9
ov000_021fae3c_L24:
    stmia r5!, {r0, r1, r2, r3}
    stmia r5!, {r0, r1, r2, r3}
    subs r4, r4, #1
    bne ov000_021fae3c_L24
    stmia r5!, {r0, r1, r2, r3}
    add r9, sp, #20
    stmia r5, {r0, r1}
    mov r0, r9
    bl native_fn_021fbc9c
    mov r0, r9
    bl native_fn_021fb7e8
    cmp r0, #255
    beq ov000_021fae3c_L1b4
    mov r0, #1
    mov r6, #0
    str r0, [sp, #0x4]
    mvn r0, #0
    mov r7, r6
    sub r8, r6, #1
    add r5, sp, #12
    add r4, sp, #16
    str r0, [sp, #0x8]
ov000_021fae3c_L7c:
    mov r0, #0
    str r0, [sp, #0xc]
    str r0, [sp, #0x10]
    cmp r6, #0
    beq ov000_021fae3c_Lc4
    ldr r0, [sp, #0x8]
    cmp r8, r0
    beq ov000_021fae3c_L1b4
    ldr r0, =0x0223716c
    mov r1, #1
    mov r9, #0
    strb r1, [r0]
    mov r0, r9
    str r0, [sp, #0x4]
    mov r0, r1
    mov r7, r8
    str r0, [sp]
    b ov000_021fae3c_Lcc
ov000_021fae3c_Lc4:
    mov r0, r9
    bl native_fn_021fbc9c
ov000_021fae3c_Lcc:
    cmp r7, #5
    addls pc, pc, r7, lsl #2
    b ov000_021fae3c_L168
    b ov000_021fae3c_Lf0
    b ov000_021fae3c_L104
    b ov000_021fae3c_L140
    b ov000_021fae3c_L168
    b ov000_021fae3c_L168
    b ov000_021fae3c_L168
ov000_021fae3c_Lf0:
    mov r0, r5
    mov r1, r4
    mov r2, r9
    bl native_fn_021fb310
    b ov000_021fae3c_L16c
ov000_021fae3c_L104:
    mov r0, #51
    mov r1, r5
    mov r2, r4
    mov r3, r9
    bl native_fn_021fadec
    mov r0, #50
    mov r1, r5
    mov r2, r4
    mov r3, r9
    bl native_fn_021fadec
    mov r0, r5
    mov r1, r4
    mov r2, r9
    bl native_fn_021fb310
    b ov000_021fae3c_L16c
ov000_021fae3c_L140:
    mov r0, #50
    mov r1, r5
    mov r2, r4
    mov r3, r9
    bl native_fn_021fadec
    mov r0, r5
    mov r1, r4
    mov r2, r9
    bl native_fn_021fb310
    b ov000_021fae3c_L16c
ov000_021fae3c_L168:
    mov r6, #1
ov000_021fae3c_L16c:
    cmp r6, #0
    bne ov000_021fae3c_L1a8
    ldr r1, [sp, #0x10]
    cmp r10, r1
    blt ov000_021fae3c_L190
    bne ov000_021fae3c_L19c
    ldr r0, [sp, #0xc]
    cmp r11, r0
    ble ov000_021fae3c_L19c
ov000_021fae3c_L190:
    mov r10, r1
    ldr r11, [sp, #0xc]
    mov r8, r7
ov000_021fae3c_L19c:
    add r0, r7, #1
    mov r0, r0, lsl #16
    mov r7, r0, asr #16
ov000_021fae3c_L1a8:
    ldr r0, [sp, #0x4]
    cmp r0, #0
    bne ov000_021fae3c_L7c
ov000_021fae3c_L1b4:
    ldr r0, [sp]
    add sp, sp, #332
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
