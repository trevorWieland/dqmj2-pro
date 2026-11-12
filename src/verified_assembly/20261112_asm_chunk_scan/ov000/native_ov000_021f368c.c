/* ov000 row 0x021f368c: 108 bytes.
 *
 * What it does: Copies a 3-register block to an optional destination under a condition in 2 predicated moves.
 *
 * Decoded shape: predicated block copy.
 *
 *   branch +0x1c -> +0x34
 *   branch +0x30 -> +0x4c
 *   test +0x18 tst r0, #1
 *   test +0x50 cmp r3, #0
 *   1 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f368c; the literal pool and
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

extern void native_fn_021dc374(void);
extern void native_fn_021dbc18(void);


asm u32 native_ov000_021f368c (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #16
    mov r3, r0
    ldrb r0, [r3, #0x162]
    mov r4, r1
    add r2, sp, #4
    tst r0, #1
    beq ov000_021f368c_L34
    add r1, r3, #528
    mov r0, r4
    mvn r3, #0
    bl native_fn_021dc374
    b ov000_021f368c_L4c
ov000_021f368c_L34:
    mvn r12, #0
    add r1, r3, #528
    mov r0, r4
    mov r3, #1
    str r12, [sp]
    bl native_fn_021dbc18
ov000_021f368c_L4c:
    mov r3, r0
    cmp r3, #0
    addne r0, sp, #4
    ldmneia r0, {r0, r1, r2}
    stmneia r4, {r0, r1, r2}
    mov r0, r3
    add sp, sp, #16
    ldmia sp!, {r4, pc}
}
