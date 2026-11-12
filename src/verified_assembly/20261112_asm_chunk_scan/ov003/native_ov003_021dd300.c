/* ov003 row 0x021dd300: 756 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (2 loads, 2 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x2e8 -> constant 0x021e0a18 (image word 0x021e0a18)
 *   pool +0x2ec -> constant 0x021e0a30 (image word 0x021e0a30)
 *   pool +0x2f0 -> native_data_021e038c (image word 0x021e038c)
 *   branch +0x24 -> +0x120
 *   branch +0x28 -> +0x38
 *   branch +0x2c -> +0x6c
 *   branch +0x30 -> +0x9c
 *   branch +0x34 -> +0xd0
 *   branch +0x68 -> +0x120
 *   branch +0x98 -> +0x120
 *   branch +0xcc -> +0x120
 *   branch +0x128 -> +0x268
 *   branch +0x13c -> +0x254
 *   branch +0x140 -> +0x150
 *   branch +0x144 -> +0x190
 *   branch +0x148 -> +0x1d0
 *   branch +0x14c -> +0x210
 *   branch +0x18c -> +0x254
 *   branch +0x1cc -> +0x254
 *   branch +0x20c -> +0x254
 *   branch +0x26c -> +0x290
 *   test +0x1c cmp r0, #3
 *   test +0x124 tst r0, #1
 *   test +0x134 cmp r0, #3
 *   test +0x268 tst r0, #2
 *   test +0x290 tst r0, #2048
 *   36 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov003.bin at 0x021dd300; the literal pool and
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

extern void native_fn_0202a634(void);
extern void native_fn_021dad9c(void);
extern void native_fn_021da3e4(void);
extern void native_fn_021da3d0(void);
extern void native_fn_020c36ac(void);
extern void native_fn_020c35ec(void);
extern void native_fn_020c360c(void);
extern void native_fn_020c362c(void);
extern void native_fn_020c364c(void);
extern void native_fn_020c366c(void);
extern void native_fn_020c368c(void);
extern void native_fn_0205e7a8(void);
extern void native_fn_021deaf8(void);
extern u8 native_data_021e038c[];
extern void native_fn_021dea38(void);


asm u32 native_ov003_021dd300 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #32
    bl native_fn_0202a634
    mov r4, r0
    bl native_fn_021dad9c
    mov r5, r0
    ldr r0, [r5]
    cmp r0, #3
    addls pc, pc, r0, lsl #2
    b ov003_021dd300_L120
    b ov003_021dd300_L38
    b ov003_021dd300_L6c
    b ov003_021dd300_L9c
    b ov003_021dd300_Ld0
ov003_021dd300_L38:
    mov r2, #2
    mov r3, #0
    mov r1, #1
    add r0, sp, #8
    str r3, [sp, #0x8]
    str r2, [sp, #0xc]
    str r3, [sp, #0x10]
    str r2, [sp, #0x14]
    str r1, [sp, #0x18]
    str r2, [sp, #0x1c]
    bl native_fn_021da3e4
    bl native_fn_021da3d0
    b ov003_021dd300_L120
ov003_021dd300_L6c:
    mov r2, #1
    mov r1, #2
    add r0, sp, #8
    str r2, [sp, #0x8]
    str r1, [sp, #0xc]
    str r2, [sp, #0x10]
    str r2, [sp, #0x14]
    str r2, [sp, #0x18]
    str r1, [sp, #0x1c]
    bl native_fn_021da3e4
    bl native_fn_021da3d0
    b ov003_021dd300_L120
ov003_021dd300_L9c:
    mov r3, #2
    mov r2, #1
    mov r1, #0
    add r0, sp, #8
    str r3, [sp, #0x8]
    str r3, [sp, #0xc]
    str r2, [sp, #0x10]
    str r3, [sp, #0x14]
    str r3, [sp, #0x18]
    str r1, [sp, #0x1c]
    bl native_fn_021da3e4
    bl native_fn_021da3d0
    b ov003_021dd300_L120
ov003_021dd300_Ld0:
    mov r0, #3
    str r0, [sp, #0x8]
    bl native_fn_020c36ac
    ldr r0, [r0, #0x4]
    str r0, [sp, #0xc]
    bl native_fn_020c36ac
    ldr r0, [r0, #0x8]
    str r0, [sp, #0x10]
    bl native_fn_020c36ac
    ldr r0, [r0, #0xc]
    str r0, [sp, #0x14]
    bl native_fn_020c36ac
    ldr r0, [r0, #0x10]
    str r0, [sp, #0x18]
    bl native_fn_020c36ac
    ldr r1, [r0, #0x14]
    add r0, sp, #8
    str r1, [sp, #0x1c]
    bl native_fn_021da3e4
    bl native_fn_021da3d0
ov003_021dd300_L120:
    ldrh r0, [r4, #2]
    tst r0, #1
    beq ov003_021dd300_L268
    ldr r0, [r5]
    and r0, r0, #255
    cmp r0, #3
    addls pc, pc, r0, lsl #2
    b ov003_021dd300_L254
    b ov003_021dd300_L150
    b ov003_021dd300_L190
    b ov003_021dd300_L1d0
    b ov003_021dd300_L210
ov003_021dd300_L150:
    mov r0, #0
    bl native_fn_020c35ec
    mov r0, #2
    bl native_fn_020c360c
    mov r0, #0
    bl native_fn_020c362c
    mov r0, #2
    bl native_fn_020c364c
    mov r0, #1
    bl native_fn_020c366c
    mov r0, #2
    bl native_fn_020c368c
    ldr r0, =0x021e0a18
    mov r1, #4
    str r1, [r0, #0xc]
    b ov003_021dd300_L254
ov003_021dd300_L190:
    mov r0, #1
    bl native_fn_020c35ec
    mov r0, #2
    bl native_fn_020c360c
    mov r0, #1
    bl native_fn_020c362c
    mov r0, #1
    bl native_fn_020c364c
    mov r0, #1
    bl native_fn_020c366c
    mov r0, #2
    bl native_fn_020c368c
    ldr r0, =0x021e0a18
    mov r1, #4
    str r1, [r0, #0xc]
    b ov003_021dd300_L254
ov003_021dd300_L1d0:
    mov r0, #2
    bl native_fn_020c35ec
    mov r0, #2
    bl native_fn_020c360c
    mov r0, #1
    bl native_fn_020c362c
    mov r0, #2
    bl native_fn_020c364c
    mov r0, #2
    bl native_fn_020c366c
    mov r0, #0
    bl native_fn_020c368c
    ldr r0, =0x021e0a18
    mov r1, #4
    str r1, [r0, #0xc]
    b ov003_021dd300_L254
ov003_021dd300_L210:
    bl native_fn_020c36ac
    mov r1, #3
    str r1, [r0]
    bl native_fn_020c36ac
    mov r5, r0
    ldr r4, =0x021e0a30
    ldmia r5!, {r0, r1, r2, r3}
    stmia r4!, {r0, r1, r2, r3}
    ldmia r5, {r0, r1}
    ldr r2, =0x021e0a18
    stmia r4, {r0, r1}
    mov r0, #1
    str r0, [r2, #0x4]
    strb r0, [r2, #0x1]
    str r0, [r2, #0xc]
    mov r0, #0
    strb r0, [r2]
ov003_021dd300_L254:
    mvn r0, #0
    mov r1, #82
    bl native_fn_0205e7a8
    add sp, sp, #32
    ldmia sp!, {r3, r4, r5, pc}
ov003_021dd300_L268:
    tst r0, #2
    beq ov003_021dd300_L290
    mov r3, #4
    ldr r2, =0x021e0a18
    sub r0, r3, #5
    mov r1, #83
    str r3, [r2, #0xc]
    bl native_fn_0205e7a8
    add sp, sp, #32
    ldmia sp!, {r3, r4, r5, pc}
ov003_021dd300_L290:
    tst r0, #2048
    addeq sp, sp, #32
    ldmeqia sp!, {r3, r4, r5, pc}
    ldr r1, [r5]
    mov r0, r5
    and r4, r1, #255
    bl native_fn_021deaf8
    mov r1, #1
    str r1, [sp]
    mov r2, #87
    ldr r0, =native_data_021e038c
    str r2, [sp, #0x4]
    mov r2, r4, lsl #1
    ldrh r2, [r0, r2]
    mov r3, r1
    mov r0, #20
    bl native_fn_021dea38
    ldr r0, =0x021e0a18
    mov r1, #3
    str r1, [r0, #0xc]
    add sp, sp, #32
    ldmia sp!, {r3, r4, r5, pc}
}
