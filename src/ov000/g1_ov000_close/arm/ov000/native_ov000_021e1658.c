/* ov000 row 0x021e1658: 276 bytes.
 *
 * What it does: 66 instructions; 9 call(s) to 0x02042cb8, 0x02042b3c, 0x021e57f0, +6 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x108 -> constant 0x022322d4 (image word 0x022322d4)
 *   pool +0x10c -> constant 0x02232344 (image word 0x02232344)
 *   pool +0x110 -> constant 0x022323e4 (image word 0x022323e4)
 *   branch +0x50 -> +0xac
 *   branch +0x60 -> +0x78
 *   branch +0x74 -> +0xac
 *   branch +0x7c -> +0x94
 *   branch +0x90 -> +0xac
 *   branch +0x98 -> +0xac
 *   branch +0xb0 -> +0xcc
 *   branch +0xd0 -> +0xf0
 *   test +0x48 cmp r4, #0
 *   test +0x4c cmpeq r0, #0
 *   test +0x5c tst r0, #8
 *   test +0x78 tst r0, #16
 *   test +0x94 tst r0, #128
 *   test +0xac cmp r4, #0
 *   test +0xc0 cmp r0, #0
 *   test +0xcc cmp r4, #0
 *   6 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e1658; the literal pool and
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

extern void native_fn_02042cb8(void);
extern void native_fn_02042b3c(void);
extern void native_fn_021e57f0(void);
extern void native_fn_021e1480(void);
extern void native_fn_021e14bc(void);
extern void native_fn_021e15e0(void);
extern void native_fn_021e8930(void);
extern void native_fn_021e0008(void);


asm u32 native_ov000_021e1658 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #12
    ldr r6, =0x022322d4
    ldr r0, [r6, #0x164]
    bl native_fn_02042cb8
    mov r5, r0
    mov r0, r6
    add r1, sp, #0
    bl native_fn_02042b3c
    ldr r1, =0x02232344
    mov r4, r0
    ldr r3, =0x022323e4
    ldmia r1, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r0, sp, #0
    mov r2, r5
    mov r1, r0
    bl native_fn_021e57f0
    cmp r4, #0
    cmpeq r0, #0
    beq ov000_021e1658_Lac
    ldr r0, [r6, #0x164]
    bl native_fn_02042cb8
    tst r0, #8
    beq ov000_021e1658_L78
    add r1, sp, #0
    mov r0, r6
    bl native_fn_021e1480
    mov r4, r0
    b ov000_021e1658_Lac
ov000_021e1658_L78:
    tst r0, #16
    beq ov000_021e1658_L94
    add r1, sp, #0
    mov r0, r6
    bl native_fn_021e14bc
    mov r4, r0
    b ov000_021e1658_Lac
ov000_021e1658_L94:
    tst r0, #128
    beq ov000_021e1658_Lac
    add r1, sp, #0
    mov r0, r6
    bl native_fn_021e15e0
    mov r4, r0
ov000_021e1658_Lac:
    cmp r4, #0
    beq ov000_021e1658_Lcc
    add r0, sp, #0
    add r1, r6, #112
    bl native_fn_021e8930
    cmp r0, #0
    moveq r4, #1
    movne r4, #0
ov000_021e1658_Lcc:
    cmp r4, #0
    beq ov000_021e1658_Lf0
    add r12, sp, #0
    add r3, r6, #112
    ldmia r12, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r3, r6, #272
    ldmia r12, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
ov000_021e1658_Lf0:
    ldr r0, =0x022322d4
    mov r1, r0
    bl native_fn_021e0008
    mov r0, r4
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, pc}
}
