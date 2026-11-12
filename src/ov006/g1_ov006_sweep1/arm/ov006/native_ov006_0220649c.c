/* ov006 row 0x0220649c: 1088 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x40c -> native_data3_0221c27c (image word 0x0221c27c)
 *   pool +0x410 -> native_data_0220bc00 (image word 0x0220bc00)
 *   pool +0x414 -> native_data_0220bbfc (image word 0x0220bbfc)
 *   pool +0x418 -> native_data_0220e958 (image word 0x0220e958)
 *   pool +0x41c -> native_data_0220bbf0 (image word 0x0220bbf0)
 *   pool +0x420 -> native_data3_0221c2c0 (image word 0x0221c2c0)
 *   pool +0x424 -> native_data3_0221c350 (image word 0x0221c350)
 *   pool +0x428 -> native_data3_0221c308 (image word 0x0221c308)
 *   pool +0x42c -> native_data6_0221c52c (image word 0x0221c52c)
 *   pool +0x430 -> native_data7_0221c64c (image word 0x0221c64c)
 *   pool +0x434 -> native_data7_0221c49c (image word 0x0221c49c)
 *   pool +0x438 -> native_data7_0221c5bc (image word 0x0221c5bc)
 *   pool +0x43c -> native_data_0220bbf4 (image word 0x0220bbf4)
 *   0 block transfer(s), 36 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x0220649c; the literal pool and
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

extern void native_fn_021e6488(void);
extern u8 native_data3_0221c27c[];
extern void native_fn_020629e0(void);
extern void native_fn_0207ca14(void);
extern void native_fn_021e6b6c(void);
extern void native_fn_02048f6c(void);
extern void native_fn_021e7ec4(void);
extern void native_fn_021e73ac(void);
extern u8 native_data_0220bc00[];
extern void native_fn_021e767c(void);
extern void native_fn_021e7b8c(void);
extern u8 native_data_0220bbfc[];
extern void native_fn_021e791c(void);
extern void native_fn_022063e8(void);
extern void native_fn_021e7268(void);
extern u8 native_data_0220e958[];
extern void native_fn_021e7210(void);
extern u8 native_data_0220bbf0[];
extern u8 native_data3_0221c2c0[];
extern void native_fn_02008c58(void);
extern void native_fn_0204b1c4(void);
extern void native_fn_0204b380(void);
extern u8 native_data3_0221c350[];
extern void native_fn_0204b4f4(void);
extern void native_fn_0204b61c(void);
extern u8 native_data3_0221c308[];
extern void native_fn_0204b628(void);
extern void native_fn_0204b770(void);
extern u8 native_data6_0221c52c[];
extern void native_fn_020485c8(void);
extern void native_fn_0204b1b0(void);
extern void native_fn_02048644(void);
extern void native_fn_02048a94(void);
extern void native_fn_02048a9c(void);
extern void native_fn_02048a60(void);
extern u8 native_data7_0221c64c[];
extern u8 native_data7_0221c49c[];
extern u8 native_data7_0221c5bc[];
extern void native_fn_022061e8(void);
extern void native_fn_02206328(void);
extern void native_fn_021eb9a4(void);
extern void native_fn_021e7d98(void);
extern u8 native_data_0220bbf4[];
extern void native_fn_021e7e90(void);
extern void native_fn_021e7e78(void);


asm u32 native_ov006_0220649c (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #28
    bl native_fn_021e6488
    ldr r0, =native_data3_0221c27c
    mov r1, #0
    str r1, [r0]
    bl native_fn_020629e0
    ldr r1, =native_data3_0221c27c
    mov r2, #0
    str r0, [r1, #0x10]
    str r2, [r1, #0x8]
    mov r0, #1
    str r2, [r1, #0x4]
    bl native_fn_0207ca14
    mov r0, #2
    bl native_fn_021e6b6c
    mov r0, #1
    bl native_fn_02048f6c
    mov r1, r0
    mov r0, #1
    bl native_fn_021e7ec4
    mov r1, #10
    str r1, [sp]
    mov r2, #2
    str r2, [sp, #0x4]
    mov r1, #0
    str r1, [sp, #0x8]
    str r0, [sp, #0xc]
    mov r0, r1
    mov r1, #15
    mov r3, #1
    bl native_fn_021e73ac
    mov r4, r0
    mov r0, #0
    ldr r1, =native_data_0220bc00
    bl native_fn_021e767c
    mov r0, #0
    bl native_fn_021e7b8c
    mov r2, #16
    str r2, [sp]
    mov r0, #2
    str r0, [sp, #0x4]
    mov r0, #0
    str r0, [sp, #0x8]
    str r4, [sp, #0xc]
    mov r0, #1
    mov r1, #4
    mov r3, #3
    bl native_fn_021e73ac
    mov r4, r0
    mov r0, #1
    bl native_fn_021e7b8c
    mov r0, #10
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r1, #2
    str r1, [sp, #0x8]
    ldr r1, =native_data_0220bbfc
    mov r2, #5
    mov r3, #0
    bl native_fn_021e791c
    mov r0, #32
    str r0, [sp]
    mov r0, #2
    str r0, [sp, #0x4]
    mov r2, #0
    str r2, [sp, #0x8]
    str r4, [sp, #0xc]
    mov r1, #3
    mov r3, #21
    bl native_fn_021e73ac
    mov r0, #2
    bl native_fn_021e7b8c
    bl native_fn_022063e8
    bl native_fn_021e7268
    ldr r0, =native_data_0220e958
    mov r1, #4
    bl native_fn_021e7210
    ldr r1, =native_data_0220bbf0
    mov r0, #0
    ldrh r3, [r1, #10]
    ldrh r12, [r1, #8]
    ldr r1, =native_data3_0221c2c0
    mov r2, #72
    strh r12, [sp, #24]
    strh r3, [sp, #26]
    bl native_fn_02008c58
    mov r3, #2
    str r3, [sp]
    mov r0, #32
    str r0, [sp, #0x4]
    ldr r0, =native_data3_0221c2c0
    mov r1, #0
    add r2, sp, #24
    bl native_fn_0204b1c4
    ldr r0, =native_data3_0221c2c0
    mov r1, #0
    bl native_fn_0204b380
    add r1, sp, #20
    mov r0, #0
    strh r0, [r1]
    strh r0, [r1, #2]
    ldr r1, =native_data3_0221c350
    mov r2, #72
    bl native_fn_02008c58
    mov r0, #2
    str r0, [sp]
    mov r0, #36
    str r0, [sp, #0x4]
    ldr r0, =native_data3_0221c350
    add r1, sp, #20
    mov r2, #56
    mov r3, #0
    bl native_fn_0204b4f4
    ldr r0, =native_data3_0221c350
    mov r1, #0
    bl native_fn_0204b61c
    add r1, sp, #16
    mov r0, #0
    strh r0, [r1]
    strh r0, [r1, #2]
    ldr r1, =native_data3_0221c308
    mov r2, #72
    bl native_fn_02008c58
    mov r3, #2
    str r3, [sp]
    mov r0, #68
    str r0, [sp, #0x4]
    ldr r0, =native_data3_0221c308
    add r1, sp, #16
    mov r2, #48
    bl native_fn_0204b628
    ldr r0, =native_data3_0221c308
    mov r1, #0
    bl native_fn_0204b770
    ldr r1, =native_data6_0221c52c
    mov r0, #0
    mov r2, #144
    bl native_fn_02008c58
    ldr r1, =native_data6_0221c52c
    mov r0, #1
    bl native_fn_020485c8
    bl native_fn_0204b1b0
    mov r1, r0
    ldr r0, =native_data6_0221c52c
    mov r2, #30
    bl native_fn_02048644
    ldr r0, =native_data6_0221c52c
    mov r1, #10
    bl native_fn_02048a94
    ldr r0, =native_data6_0221c52c
    mov r1, #3
    bl native_fn_02048a9c
    ldr r0, =native_data6_0221c52c
    mov r1, #136
    ldr r3, [r0, #0x7c]
    mov r2, #24
    orr r3, r3, #2
    str r3, [r0, #0x7c]
    bl native_fn_02048a60
    mov r0, #0
    ldr r1, =native_data7_0221c64c
    mov r2, #144
    bl native_fn_02008c58
    mov r0, #1
    ldr r1, =native_data7_0221c64c
    bl native_fn_020485c8
    bl native_fn_0204b1b0
    mov r1, r0
    ldr r0, =native_data7_0221c64c
    mov r2, #63
    bl native_fn_02048644
    ldr r0, =native_data7_0221c64c
    mov r1, #208
    mov r2, #40
    bl native_fn_02048a60
    ldr r0, =native_data7_0221c64c
    mov r1, #10
    bl native_fn_02048a94
    ldr r0, =native_data7_0221c64c
    mov r1, #3
    bl native_fn_02048a9c
    ldr r2, =native_data7_0221c64c
    mov r0, #0
    ldr r3, [r2, #0x7c]
    ldr r1, =native_data7_0221c49c
    orr r3, r3, #2
    str r3, [r2, #0x7c]
    mov r2, #144
    bl native_fn_02008c58
    mov r0, #1
    ldr r1, =native_data7_0221c49c
    bl native_fn_020485c8
    bl native_fn_0204b1b0
    mov r1, r0
    ldr r0, =native_data7_0221c49c
    mov r2, #72
    bl native_fn_02048644
    ldr r0, =native_data7_0221c49c
    mov r1, #208
    mov r2, #40
    bl native_fn_02048a60
    ldr r0, =native_data7_0221c49c
    mov r1, #10
    bl native_fn_02048a94
    ldr r0, =native_data7_0221c49c
    mov r1, #3
    bl native_fn_02048a9c
    ldr r2, =native_data7_0221c49c
    ldr r1, =native_data7_0221c5bc
    ldr r3, [r2, #0x7c]
    mov r0, #0
    bic r3, r3, #2
    str r3, [r2, #0x7c]
    mov r2, #144
    bl native_fn_02008c58
    mov r0, #1
    ldr r1, =native_data7_0221c5bc
    bl native_fn_020485c8
    bl native_fn_0204b1b0
    mov r1, r0
    ldr r0, =native_data7_0221c5bc
    mov r2, #67
    bl native_fn_02048644
    ldr r0, =native_data7_0221c5bc
    mov r1, #128
    mov r2, #96
    bl native_fn_02048a60
    ldr r0, =native_data7_0221c5bc
    mov r1, #10
    bl native_fn_02048a94
    ldr r0, =native_data7_0221c5bc
    mov r1, #3
    bl native_fn_02048a9c
    ldr r1, =native_data7_0221c5bc
    mov r0, #0
    ldr r2, [r1, #0x7c]
    orr r2, r2, #2
    str r2, [r1, #0x7c]
    bl native_fn_022061e8
    mov r0, #0
    mov r1, r0
    bl native_fn_02206328
    mov r0, #12
    mov r1, #1
    mov r2, #0
    bl native_fn_021eb9a4
    mov r0, #1
    bl native_fn_021e7d98
    ldr r0, =native_data_0220bbf4
    bl native_fn_021e7e90
    mov r0, #1
    bl native_fn_021e7e78
    mov r1, #0
    ldr r0, =native_data3_0221c27c
    str r1, [r0, #0x8]
    add sp, sp, #28
    ldmia sp!, {r3, r4, pc}
}
