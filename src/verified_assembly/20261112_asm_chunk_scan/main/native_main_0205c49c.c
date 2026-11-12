/* main row 0x0205c49c: 380 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (2 loads, 2 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x174 -> native_data_020da06c (image word 0x020da06c)
 *   pool +0x178 -> native_data_020ddbb0 (image word 0x020ddbb0)
 *   branch +0x5c -> +0x168
 *   branch +0x80 -> +0x98
 *   branch +0x94 -> +0x150
 *   branch +0x9c -> +0xb4
 *   branch +0xb0 -> +0x150
 *   branch +0xb8 -> +0xd0
 *   branch +0xcc -> +0x150
 *   branch +0xd4 -> +0xf0
 *   branch +0xec -> +0x150
 *   branch +0xf4 -> +0x13c
 *   branch +0x10c -> +0x130
 *   branch +0x11c -> +0x130
 *   branch +0x138 -> +0x150
 *   branch +0x140 -> +0x150
 *   branch +0x154 -> +0x168
 *   test +0x7c cmp r5, #1
 *   test +0x98 cmp r5, #2
 *   test +0xb4 cmp r5, #3
 *   test +0xd0 cmp r5, #0
 *   test +0xf0 cmp r5, #4
 *   test +0x108 cmp r0, #0
 *   test +0x114 cmp r0, #0
 *   test +0x13c cmp r5, #5
 *   test +0x150 cmp r4, #0
 *   2 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0205c49c; the literal pool and
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

extern u8 native_data_020da06c[];
extern u8 native_data_020ddbb0[];
extern void native_fn_0201d444(void);
extern void native_fn_02040c90(void);
extern void native_fn_02040d34(void);
extern void native_fn_02040ce8(void);
extern void native_fn_020411f4(void);
extern void native_fn_02040e0c(void);
extern void native_fn_02040fb0(void);
extern void native_fn_02040e74(void);
extern void native_fn_02008ca4(void);


asm u32 native_main_0205c49c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #40
    ldr r12, =native_data_020da06c
    add r8, sp, #0
    mov r7, r0
    mov r6, r1
    mov lr, r2
    mov r5, r3
    mov r4, r8
    ldmia r12!, {r0, r1, r2, r3}
    stmia r8!, {r0, r1, r2, r3}
    ldmia r12, {r0, r1}
    stmia r8, {r0, r1}
    ldr r3, [r4, r5, lsl #2]
    ldr r1, =native_data_020ddbb0
    mov r2, lr
    add r0, sp, #24
    mov r4, #0
    bl native_fn_0201d444
    mov r0, r7
    add r1, sp, #24
    bl native_fn_02040c90
    movs r8, r0
    bmi main_0205c49c_L168
    mov r0, r7
    mov r1, r8
    bl native_fn_02040d34
    mov r0, r7
    mov r1, r8
    bl native_fn_02040ce8
    mov r7, r0
    cmp r5, #1
    bne main_0205c49c_L98
    mov r1, r7
    add r0, r6, #104
    bl native_fn_020411f4
    mov r4, r0
    b main_0205c49c_L150
main_0205c49c_L98:
    cmp r5, #2
    bne main_0205c49c_Lb4
    mov r1, r7
    add r0, r6, #108
    bl native_fn_020411f4
    mov r4, r0
    b main_0205c49c_L150
main_0205c49c_Lb4:
    cmp r5, #3
    bne main_0205c49c_Ld0
    mov r1, r7
    add r0, r6, #112
    bl native_fn_020411f4
    mov r4, r0
    b main_0205c49c_L150
main_0205c49c_Ld0:
    cmp r5, #0
    bne main_0205c49c_Lf0
    mov r1, r7
    add r0, r6, #16
    mov r2, #1
    bl native_fn_02040e0c
    mov r4, r0
    b main_0205c49c_L150
main_0205c49c_Lf0:
    cmp r5, #4
    bne main_0205c49c_L13c
    ldr r2, [sp, #0x40]
    mov r1, r7
    add r0, r6, #16
    bl native_fn_02040fb0
    cmp r0, #0
    beq main_0205c49c_L130
    ldr r0, [sp, #0x40]
    cmp r0, #0
    movne r4, #1
    bne main_0205c49c_L130
    mov r1, r7
    add r0, r6, #16
    bl native_fn_02040e74
    mov r4, r0
main_0205c49c_L130:
    ldr r0, [sp, #0x40]
    strb r0, [r6, #0x8]
    b main_0205c49c_L150
main_0205c49c_L13c:
    cmp r5, #5
    bne main_0205c49c_L150
    add r1, r6, #116
    mov r2, #56
    bl native_fn_02008ca4
main_0205c49c_L150:
    cmp r4, #0
    beq main_0205c49c_L168
    ldr r1, [r6, #0xc]
    mov r0, #1
    orr r0, r1, r0, lsl r5
    str r0, [r6, #0xc]
main_0205c49c_L168:
    mov r0, r4
    add sp, sp, #40
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
