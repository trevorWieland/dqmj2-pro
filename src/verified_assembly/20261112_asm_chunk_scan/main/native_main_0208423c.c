/* main row 0x0208423c: 224 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (one load, one store).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0xdc -> constant 0x021c9600 (image word 0x021c9600)
 *   branch +0x20 -> +0x6c
 *   branch +0x2c -> +0x58
 *   branch +0x40 -> +0x58
 *   branch +0x54 -> +0x6c
 *   back edge +0x68 -> +0x24
 *   branch +0x94 -> +0xc8
 *   back edge +0xb4 -> +0xa8
 *   back edge +0xd4 -> +0x8c
 *   test +0x18 cmp r1, #0
 *   test +0x28 cmp r0, #0
 *   test +0x3c cmp r0, #0
 *   test +0x64 cmp r4, r0
 *   test +0x6c cmp r5, #0
 *   test +0x84 cmp r1, #0
 *   test +0x90 cmp r0, #0
 *   test +0xcc cmp r2, r1
 *   3 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0208423c; the literal pool and
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

extern void native_fn_02084508(void);


asm u32 native_main_0208423c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    ldr r8, =0x021c9600
    mov r5, #0
    ldrb r1, [r8]
    mov r7, r0
    mov r4, r5
    cmp r1, #0
    ldr r6, [r8, #0x18]
    ble main_0208423c_L6c
main_0208423c_L24:
    ldrb r0, [r6, #0xc0]
    cmp r0, #0
    beq main_0208423c_L58
    add r0, r6, #4
    add r1, r7, #4
    bl native_fn_02084508
    cmp r0, #0
    beq main_0208423c_L58
    ldr r0, =0x021c9600
    mov r5, #1
    ldrh r0, [r0, #6]
    strh r0, [r6, #194]
    b main_0208423c_L6c
main_0208423c_L58:
    ldrb r0, [r8]
    add r4, r4, #1
    add r6, r6, #196
    cmp r4, r0
    blt main_0208423c_L24
main_0208423c_L6c:
    cmp r5, #0
    ldmneia sp!, {r4, r5, r6, r7, r8, pc}
    ldr r0, =0x021c9600
    mov r2, #0
    ldrb r1, [r0]
    ldr r6, [r0, #0x18]
    cmp r1, #0
    ldmleia sp!, {r4, r5, r6, r7, r8, pc}
main_0208423c_L8c:
    ldrb r0, [r6, #0xc0]
    cmp r0, #0
    bne main_0208423c_Lc8
    mov r0, #1
    mov r5, r6
    strb r0, [r6, #0xc0]
    mov r4, #12
main_0208423c_La8:
    ldmia r7!, {r0, r1, r2, r3}
    stmia r5!, {r0, r1, r2, r3}
    subs r4, r4, #1
    bne main_0208423c_La8
    ldr r0, =0x021c9600
    ldrh r0, [r0, #6]
    strh r0, [r6, #194]
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
main_0208423c_Lc8:
    add r2, r2, #1
    cmp r2, r1
    add r6, r6, #196
    blt main_0208423c_L8c
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
