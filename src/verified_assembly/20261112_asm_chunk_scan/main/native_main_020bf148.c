/* main row 0x020bf148: 208 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (2 loads, 2 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0xc8 -> constant 0x021d44b4 (image word 0x021d44b4)
 *   pool +0xcc -> constant 0x021d423c (image word 0x021d423c)
 *   branch +0x2c -> +0x84
 *   branch +0x48 -> +0x74
 *   back edge +0x60 -> +0x54
 *   back edge +0x80 -> +0x3c
 *   back edge +0xc0 -> +0xa4
 *   test +0x28 cmp r6, #0
 *   test +0x44 cmp r0, #0
 *   test +0x7c cmp r5, r6
 *   test +0x88 cmp r7, #3
 *   test +0xbc cmp r7, #3
 *   1 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020bf148; the literal pool and
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

extern void native_fn_02008d78(void);


asm u32 native_main_020bf148 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    ldr r1, =0x021d44b4
    mov r2, #616
    mla r0, r2, r0, r1
    mov r1, #0
    bl native_fn_02008d78
    ldr r0, =0x021d423c
    mov r7, #0
    ldrb r6, [r0, #0x1]
    mov r5, r7
    cmp r6, #0
    bls main_020bf148_L84
    mov r8, #616
    ldr lr, =0x021d44b4
    mov r9, r8
main_020bf148_L3c:
    mla r4, r5, r9, r14
    ldrb r0, [r4, #0xaf]
    cmp r0, #0
    beq main_020bf148_L74
    mla r12, r7, r8, r14
    mov r10, #38
main_020bf148_L54:
    ldmia r4!, {r0, r1, r2, r3}
    stmia r12!, {r0, r1, r2, r3}
    subs r10, r10, #1
    bne main_020bf148_L54
    add r2, r7, #1
    ldmia r4, {r0, r1}
    stmia r12, {r0, r1}
    and r7, r2, #255
main_020bf148_L74:
    add r0, r5, #1
    and r5, r0, #255
    cmp r5, r6
    blo main_020bf148_L3c
main_020bf148_L84:
    ldr r0, =0x021d423c
    cmp r7, #3
    strb r7, [r0, #0x1]
    ldmhsia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
    mov r5, #616
    ldr r8, =0x021d44b4
    mov r6, #0
    mov r4, r5
main_020bf148_La4:
    mla r0, r7, r4, r8
    mov r1, r6
    mov r2, r5
    bl native_fn_02008d78
    add r0, r7, #1
    and r7, r0, #255
    cmp r7, #3
    blo main_020bf148_La4
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
