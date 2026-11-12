/* main row 0x020d19d4: 552 bytes.
 *
 * What it does: Writes one block of 8 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x20c -> constant 0x021d7070 (image word 0x021d7070)
 *   pool +0x210 -> native_data_020e32ac (image word 0x020e32ac)
 *   pool +0x214 -> native_data_020e30d8 (image word 0x020e30d8)
 *   pool +0x218 -> constant 0x021d7090 (image word 0x021d7090)
 *   pool +0x21c -> constant 0x92492493 (image word 0x92492493)
 *   pool +0x220 -> constant 0x38e38e39 (image word 0x38e38e39)
 *   pool +0x224 -> constant 0x021d7094 (image word 0x021d7094)
 *   branch +0x38 -> +0x190
 *   branch +0x4c -> +0x190
 *   back edge +0x88 -> +0x6c
 *   branch +0x98 -> +0x154
 *   branch +0xec -> +0xfc
 *   branch +0x13c -> +0x1d0
 *   branch +0x150 -> +0x1d0
 *   branch +0x18c -> +0x1d0
 *   branch +0x19c -> +0x1b8
 *   branch +0x1b4 -> +0x1d0
 *   test +0x34 cmp r0, #8
 *   test +0x48 cmp r0, #0
 *   test +0x78 cmp r0, #0
 *   test +0x84 cmp r7, #47
 *   test +0x94 cmp r0, #0
 *   test +0xdc cmp r0, #22
 *   test +0x124 cmp r7, r1
 *   test +0x138 cmp r5, r0
 *   test +0x198 cmp r0, #0
 *   11 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020d19d4; the literal pool and
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

extern void native_fn_0209b040(void);
extern void native_fn_0209af04(void);
extern u8 native_data_020e32ac[];
extern void native_fn_0201d984(void);
extern void native_fn_0201f274(void);
extern u8 native_data_020e30d8[];
extern void native_fn_020d1cf8(void);
extern void native_fn_020d1958(void);
extern void native_fn_0203d294(void);
extern void native_fn_02048094(void);
extern void native_fn_020d1bfc(void);
extern void native_fn_020d1fcc(void);


asm u32 native_main_020d19d4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    sub sp, sp, #88
    add r0, sp, #72
    add r1, sp, #60
    mov r4, #5
    blx native_fn_0209b040
    add r0, sp, #0
    blx native_fn_0209af04
    ldr r0, =0x021d7070
    mvn r1, #0
    str r1, [r0, #0x10]
    str r1, [r0, #0xc]
    ldr r0, [sp]
    cmp r0, #8
    bne main_020d19d4_L190
    ldr r1, =native_data_020e32ac
    add r0, sp, #8
    bl native_fn_0201d984
    cmp r0, #0
    beq main_020d19d4_L190
    add r0, sp, #14
    bl native_fn_0201f274
    ldr r4, =0x021d7070
    ldr r5, =native_data_020e30d8
    mov r7, #1
    str r0, [r4, #0x10]
    add r6, sp, #12
main_020d19d4_L6c:
    ldr r1, [r5, r7, lsl #2]
    mov r0, r6
    bl native_fn_0201d984
    cmp r0, #0
    strne r7, [r4, #0xc]
    add r7, r7, #1
    cmp r7, #47
    blt main_020d19d4_L6c
    ldr r0, =0x021d7090
    bl native_fn_020d1cf8
    cmp r0, #0
    blt main_020d19d4_L154
    ldr r4, =0x92492493
    ldr r3, =0x38e38e39
    smull r2, r1, r4, r0
    smull r2, r5, r3, r0
    mov r12, r0, lsr #31
    add r1, r0, r1
    add r5, r12, r5, asr #1
    mov r4, #9
    smull r2, r3, r4, r5
    add r1, r12, r1, asr #2
    mov r4, #7
    smull r1, r3, r4, r1
    ldr r3, =0x021d7070
    sub r5, r0, r2
    sub r1, r0, r1
    ldr r0, [r3, #0xc]
    cmp r0, #22
    movgt r2, #3
    strgt r2, [r3, #0x1c]
    movgt r4, #4
    bgt main_020d19d4_Lfc
    mov r2, #2
    str r2, [r3, #0x1c]
    mov r4, #3
main_020d19d4_Lfc:
    ldr lr, =0x021d7070
    ldr r3, =0x92492493
    ldr r6, [lr, #0x10]
    mov r12, #7
    smull r2, r7, r3, r6
    add r7, r6, r7
    mov r2, r6, lsr #31
    add r7, r2, r7, asr #2
    smull r2, r3, r12, r7
    sub r7, r6, r2
    cmp r7, r1
    moveq r1, #0
    streq r1, [lr, #0x1c]
    moveq r4, #1
    bl native_fn_020d1958
    cmp r5, r0
    bne main_020d19d4_L1d0
    ldr r0, =0x021d7070
    mov r1, #1
    str r1, [r0, #0x1c]
    mov r4, #2
    b main_020d19d4_L1d0
main_020d19d4_L154:
    ldr r1, =0x92492493
    rsb r3, r0, #0
    smull r0, r4, r1, r3
    add r4, r3, r4
    mov r0, r3, lsr #31
    add r4, r0, r4, asr #2
    mov r2, #7
    smull r0, r1, r2, r4
    sub r4, r3, r0
    rsb r1, r4, #6
    ldr r0, =0x021d7070
    add r1, r1, #4
    str r1, [r0, #0x1c]
    mov r4, #5
    b main_020d19d4_L1d0
main_020d19d4_L190:
    ldr r0, =0x021d7094
    bl native_fn_020d1cf8
    cmp r0, #0
    blt main_020d19d4_L1b8
    mov r0, #5
    bl native_fn_0203d294
    ldr r1, =0x021d7070
    add r0, r0, #11
    str r0, [r1, #0x1c]
    b main_020d19d4_L1d0
main_020d19d4_L1b8:
    mov r0, #7
    bl native_fn_0203d294
    ldr r1, =0x021d7070
    add r0, r0, #16
    str r0, [r1, #0x1c]
    mov r4, #0
main_020d19d4_L1d0:
    ldr r0, =0x021d7070
    mov r1, #0
    ldr r0, [r0, #0xc]
    bl native_fn_02048094
    ldr r0, =0x021d7070
    mov r1, #32
    ldr r0, [r0, #0x10]
    bl native_fn_02048094
    bl native_fn_020d1bfc
    ldr r0, =0x021d7070
    ldr r0, [r0, #0x1c]
    bl native_fn_020d1fcc
    mov r0, r4
    add sp, sp, #88
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
