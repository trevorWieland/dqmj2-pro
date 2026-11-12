/* ov006 row 0x021ea7d8: 1004 bytes.
 *
 * What it does: Writes 3 blocks of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x3b4 -> native_data_02208774 (image word 0x02208774)
 *   pool +0x3b8 -> native_data_02208540 (image word 0x02208540)
 *   pool +0x3bc -> native_data_0220853c (image word 0x0220853c)
 *   pool +0x3c0 -> native_data_02208538 (image word 0x02208538)
 *   pool +0x3c4 -> native_data_02208534 (image word 0x02208534)
 *   pool +0x3c8 -> constant 0x000f423f (image word 0x000f423f)
 *   pool +0x3cc -> native_data_02208580 (image word 0x02208580)
 *   pool +0x3d0 -> native_data_02208530 (image word 0x02208530)
 *   pool +0x3d4 -> native_data_0220852c (image word 0x0220852c)
 *   pool +0x3d8 -> native_data_02208508 (image word 0x02208508)
 *   pool +0x3dc -> constant 0x0000270f (image word 0x0000270f)
 *   pool +0x3e0 -> native_data_02208528 (image word 0x02208528)
 *   pool +0x3e4 -> native_data_02208524 (image word 0x02208524)
 *   pool +0x3e8 -> native_data_02208520 (image word 0x02208520)
 *   back edge +0x8c -> +0x5c
 *   branch +0x164 -> +0x1a0
 *   branch +0x19c -> +0x1c4
 *   test +0x88 cmp r9, #13
 *   test +0x15c cmp r0, #0
 *   test +0x174 cmp r1, r0
 *   test +0x1d0 cmp r1, r0
 *   test +0x298 cmp r1, r0
 *   test +0x2cc cmp r5, r0
 *   test +0x35c cmp r1, #99
 *   3 block transfer(s), 39 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ea7d8; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021e7370(void);
extern void native_fn_021e6bdc(void);
extern void native_fn_021e5738(void);
extern void native_fn_021e5740(void);
extern void native_fn_021e5748(void);
extern void native_fn_02048f6c(void);
extern void native_fn_021e7ec4(void);
extern u8 native_data_02208774[];
extern void native_fn_021e73ac(void);
extern u8 native_data_02208540[];
extern void native_fn_021e767c(void);
extern void native_fn_021e76f0(void);
extern u8 native_data_0220853c[];
extern void native_fn_021e7b64(void);
extern void native_fn_021e796c(void);
extern void native_fn_021e92bc(void);
extern void native_fn_021e791c(void);
extern u8 native_data_02208538[];
extern u8 native_data_02208534[];
extern void native_fn_021e952c(void);
extern void native_fn_021e78ac(void);
extern u8 native_data_02208580[];
extern void native_fn_021e7824(void);
extern u8 native_data_02208530[];
extern u8 native_data_0220852c[];
extern u8 native_data_02208508[];
extern u8 native_data_02208528[];
extern u8 native_data_02208524[];
extern u8 native_data_02208520[];


asm u32 native_ov006_021ea7d8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    mvn r0, #0
    bl native_fn_021e7370
    mov r0, #9
    bl native_fn_021e6bdc
    bl native_fn_021e5738
    mov r6, r0
    bl native_fn_021e5740
    mov r11, r0
    bl native_fn_021e5748
    ldr r1, [r6, #0x4]
    mov r7, r0
    mov r0, #0
    bic r8, r1, #-2147483648
    bl native_fn_02048f6c
    mov r1, r0
    mov r0, #0
    bl native_fn_021e7ec4
    ldr r10, =native_data_02208774
    mov r9, #0
    mov r5, #1
    mov r4, #16
ov006_021ea7d8_L5c:
    ldrsb r2, [r10, #6]
    mov r1, r4
    str r2, [sp]
    ldrsb r2, [r10, #7]
    stmib sp, {r2, r5}
    str r0, [sp, #0xc]
    ldrsb r2, [r10, #4]
    ldrsb r3, [r10, #5]
    ldr r0, [r10], #8
    bl native_fn_021e73ac
    add r9, r9, #1
    cmp r9, #13
    blo ov006_021ea7d8_L5c
    ldr r1, =native_data_02208540
    mov r0, #36
    bl native_fn_021e767c
    add r1, r6, #16
    mov r0, #37
    bl native_fn_021e76f0
    ldr r1, =native_data_0220853c
    mov r0, #39
    bl native_fn_021e767c
    mov r0, #36
    bl native_fn_021e7b64
    mov r0, #37
    bl native_fn_021e7b64
    mov r0, #39
    bl native_fn_021e7b64
    mov r0, #42
    bl native_fn_021e7b64
    mov r0, #38
    bl native_fn_021e7b64
    mov r2, #0
    ldr r1, [r6, #0x8]
    mov r0, #38
    mov r3, r2
    bl native_fn_021e796c
    mov r0, r8
    bl native_fn_021e92bc
    mov r1, r0
    mov r0, #14
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r2, #0
    str r0, [sp, #0x8]
    mov r0, #42
    mov r3, r2
    bl native_fn_021e791c
    ldr r1, =native_data_02208538
    mov r0, #40
    bl native_fn_021e767c
    ldr r1, =native_data_02208534
    mov r0, #41
    bl native_fn_021e767c
    mov r0, #40
    bl native_fn_021e7b64
    mov r0, #41
    bl native_fn_021e7b64
    mov r0, #43
    bl native_fn_021e7b64
    mov r0, #44
    bl native_fn_021e7b64
    bl native_fn_021e952c
    cmp r0, #0
    mov r4, #1
    beq ov006_021ea7d8_L1a0
    ldr r1, [r11, #0x4]
    ldr r0, =0x000f423f
    mov r3, #0
    cmp r1, r0
    movhs r1, r0
    str r3, [sp]
    mov r0, #12
    str r0, [sp, #0x4]
    str r4, [sp, #0x8]
    mov r0, #43
    mov r2, #6
    str r4, [sp, #0xc]
    bl native_fn_021e78ac
    b ov006_021ea7d8_L1c4
ov006_021ea7d8_L1a0:
    mov r0, #12
    str r0, [sp]
    mov r2, #0
    str r4, [sp, #0x4]
    ldr r1, =native_data_02208580
    mov r3, r2
    mov r0, #43
    str r4, [sp, #0x8]
    bl native_fn_021e7824
ov006_021ea7d8_L1c4:
    ldr r1, [r11, #0x8]
    ldr r0, =0x000f423f
    mov r3, #0
    cmp r1, r0
    movhs r1, r0
    str r3, [sp]
    mov r0, #12
    str r0, [sp, #0x4]
    mov r4, #1
    str r4, [sp, #0x8]
    mov r0, #44
    mov r2, #6
    str r4, [sp, #0xc]
    bl native_fn_021e78ac
    mov r0, #2
    stmia sp, {r0, r4}
    ldr r1, =native_data_02208530
    mov r0, #43
    mov r2, #12
    mov r3, #0
    str r4, [sp, #0x8]
    bl native_fn_021e791c
    mov r0, #2
    str r0, [sp]
    mov r3, r4
    str r3, [sp, #0x4]
    str r3, [sp, #0x8]
    ldr r1, =native_data_02208530
    mov r0, #44
    mov r2, #12
    mov r3, #0
    bl native_fn_021e791c
    ldr r1, =native_data_0220852c
    mov r0, #45
    bl native_fn_021e767c
    ldr r1, =native_data_02208508
    mov r0, #46
    bl native_fn_021e767c
    mov r0, #45
    bl native_fn_021e7b64
    mov r0, #46
    bl native_fn_021e7b64
    mov r0, #47
    bl native_fn_021e7b64
    mov r0, #48
    bl native_fn_021e7b64
    mov r0, #20
    mul r4, r8, r0
    add r0, r7, r4
    ldr r1, [r0, #0xc]
    ldr r2, [r0, #0x8]
    ldr r0, =0x0000270f
    sub r5, r2, r1
    cmp r1, r0
    movhs r1, r0
    mov r0, #0
    str r0, [sp]
    mov r2, #4
    str r2, [sp, #0x4]
    mov r6, #1
    str r6, [sp, #0x8]
    mov r0, #47
    mov r3, #6
    str r6, [sp, #0xc]
    bl native_fn_021e78ac
    ldr r0, =0x0000270f
    cmp r5, r0
    movhs r5, r0
    mov r0, #0
    str r0, [sp]
    mov r2, #4
    str r2, [sp, #0x4]
    mov r6, #1
    str r6, [sp, #0x8]
    mov r1, r5
    mov r0, #47
    mov r3, #12
    str r6, [sp, #0xc]
    bl native_fn_021e78ac
    mov r0, #2
    str r0, [sp]
    mov r5, r6
    str r5, [sp, #0x4]
    ldr r1, =native_data_02208528
    mov r0, #47
    mov r2, #10
    mov r3, #0
    str r5, [sp, #0x8]
    bl native_fn_021e791c
    mov r0, #2
    str r0, [sp]
    mov r3, r6
    str r3, [sp, #0x4]
    str r3, [sp, #0x8]
    ldr r1, =native_data_02208524
    mov r0, #47
    mov r2, #16
    mov r3, #0
    bl native_fn_021e791c
    add r0, r7, r4
    ldr r1, [r0, #0x10]
    mov r3, #0
    cmp r1, #99
    str r3, [sp]
    mov r0, #12
    str r0, [sp, #0x4]
    mov r4, #1
    str r4, [sp, #0x8]
    movhs r1, #99
    mov r0, #48
    mov r2, #6
    str r4, [sp, #0xc]
    bl native_fn_021e78ac
    mov r0, #2
    stmia sp, {r0, r4}
    ldr r1, =native_data_02208520
    mov r0, #48
    mov r2, #12
    mov r3, #0
    str r4, [sp, #0x8]
    bl native_fn_021e791c
    mov r0, r4
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
