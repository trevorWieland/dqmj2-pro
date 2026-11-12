/* ov001 row 0x02207db8: 484 bytes.
 *
 * What it does: 121 instructions; 18 call(s) to 0x02207938, 0x02049f4c, 0x02049ffc, +15 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, pc}
 *
 * Decoded shape: loop with 18 calls (121 instructions, 18 calls, 13 branches, 18 back edges, 0 literal slots).
 *
 *   branch +0x2c -> +0x1c8
 *   branch +0x30 -> +0x40
 *   branch +0x34 -> +0x94
 *   branch +0x38 -> +0xe8
 *   branch +0x3c -> +0x1c8
 *   branch +0x60 -> +0x7c
 *   branch +0x78 -> +0x1c8
 *   branch +0x90 -> +0x1c8
 *   branch +0xa4 -> +0xd0
 *   branch +0xcc -> +0x1c8
 *   branch +0xe4 -> +0x1c8
 *   back edge +0x128 -> +0xf8
 *   branch +0x14c -> +0x17c
 *   branch +0x178 -> +0x1c8
 *   test +0x24 cmp r0, #3
 *   test +0x58 cmp r0, #0
 *   test +0x5c cmpne r0, #2
 *   test +0xa0 cmp r2, r0
 *   test +0x104 cmp r2, #6
 *   test +0x120 cmp r3, #2
 *   test +0x148 cmp r6, #0
 *   0 block transfer(s), 19 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02207db8; the literal pool and
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

extern void native_fn_02207938(void);
extern void native_fn_02049f4c(void);
extern void native_fn_02049ffc(void);
extern void native_fn_021fe6cc(void);
extern void native_fn_02207d58(void);
extern void native_fn_0220795c(void);
extern void native_fn_0204a010(void);
extern void native_fn_02049f90(void);
extern void native_fn_021fe4ac(void);
extern void native_fn_021f949c(void);


asm u32 native_ov001_02207db8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #20
    bl native_fn_02207938
    mov r4, r0
    ldr r0, [r4, #0x8]
    ldr r1, [r0]
    ldr r5, [r1, #0x4]
    bl native_fn_02049f4c
    ldr r0, [r4, #0x20]
    cmp r0, #3
    addls pc, pc, r0, lsl #2
    b ov001_02207db8_L1c8
    b ov001_02207db8_L40
    b ov001_02207db8_L94
    b ov001_02207db8_Le8
    b ov001_02207db8_L1c8
ov001_02207db8_L40:
    mov r0, r5
    bl native_fn_02049ffc
    ldr r0, [r4, #0xc]
    bl native_fn_021fe6cc
    bl native_fn_02207d58
    ldr r0, [r4, #0x24]
    cmp r0, #0
    cmpne r0, #2
    bne ov001_02207db8_L7c
    mov r0, #1
    str r0, [r4, #0x20]
    mov r0, #2
    str r0, [r4, #0x540]
    bl native_fn_0220795c
    b ov001_02207db8_L1c8
ov001_02207db8_L7c:
    mov r0, r5
    bl native_fn_02049ffc
    bl native_fn_02207d58
    mov r0, #2
    str r0, [r4, #0x20]
    b ov001_02207db8_L1c8
ov001_02207db8_L94:
    ldr r1, [r4, #0x540]
    ldr r0, [r4, #0x544]
    add r2, r1, #10
    cmp r2, r0
    bge ov001_02207db8_Ld0
    add r3, r1, #12
    mov r1, #0
    mov r0, r5
    mov r2, r1
    str r3, [r4, #0x540]
    mov r5, #112
    mov r3, #240
    str r5, [sp]
    bl native_fn_0204a010
    b ov001_02207db8_L1c8
ov001_02207db8_Ld0:
    mov r0, r5
    bl native_fn_02049ffc
    bl native_fn_02207d58
    mov r0, #2
    str r0, [r4, #0x20]
    b ov001_02207db8_L1c8
ov001_02207db8_Le8:
    mov r3, #0
    mov r12, r4
    mov r6, #1
    mov r1, r3
ov001_02207db8_Lf8:
    ldrsh r2, [r12, #110]
    ldrsh r0, [r12, #112]
    sub r2, r2, r0
    cmp r2, #6
    addgt r0, r0, #6
    strgth r0, [r12, #112]
    add r0, r3, #1
    mov r0, r0, lsl #24
    mov r3, r0, asr #24
    movgt r6, r1
    cmp r3, #2
    add r12, r12, #70
    blt ov001_02207db8_Lf8
    mov r1, #0
    mov r12, #112
    mov r0, r5
    mov r2, r1
    mov r3, #240
    str r12, [sp]
    bl native_fn_0204a010
    cmp r6, #0
    bne ov001_02207db8_L17c
    mov r0, #2
    str r0, [sp]
    mov r1, #1
    str r1, [sp, #0x4]
    ldr r0, [r5, #0x58]
    mov r2, #11
    str r0, [sp, #0x8]
    ldr r0, [r4, #0x8]
    mov r3, #30
    bl native_fn_02049f90
    b ov001_02207db8_L1c8
ov001_02207db8_L17c:
    mov r0, r5
    bl native_fn_02049ffc
    bl native_fn_02207d58
    mov r1, #0
    str r1, [r4, #0x20]
    mov r0, #19
    str r0, [sp]
    mov r0, #30
    str r0, [sp, #0x4]
    mov r0, #2
    str r0, [sp, #0x8]
    str r1, [sp, #0xc]
    mov r3, #1
    mov r0, #28
    mov r1, #8
    mov r2, #127
    str r3, [sp, #0x10]
    bl native_fn_021fe4ac
    str r0, [r4, #0xc]
ov001_02207db8_L1c8:
    mov r0, #82
    mov r1, #1
    bl native_fn_021f949c
    mov r0, #0
    str r0, [r4, #0x1c]
    add sp, sp, #20
    ldmia sp!, {r3, r4, r5, r6, pc}
}
