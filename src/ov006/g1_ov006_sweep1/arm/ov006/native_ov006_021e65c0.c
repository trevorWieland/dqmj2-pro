/* ov006 row 0x021e65c0: 396 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x164 -> native_data5_02218d90 (image word 0x02218d90)
 *   pool +0x168 -> native_data_0220d114 (image word 0x0220d114)
 *   pool +0x16c -> constant 0x05000400 (image word 0x05000400)
 *   pool +0x170 -> constant 0x07000400 (image word 0x07000400)
 *   pool +0x174 -> native_data_0220d308 (image word 0x0220d308)
 *   pool +0x178 -> constant 0x020daf0c (image word 0x020daf0c)
 *   pool +0x17c -> constant 0x020daef8 (image word 0x020daef8)
 *   pool +0x180 -> native_data_0220d314 (image word 0x0220d314)
 *   pool +0x184 -> constant 0x020dc368 (image word 0x020dc368)
 *   pool +0x188 -> constant 0x020dc348 (image word 0x020dc348)
 *   test +0x24 cmp r0, #9
 *   test +0x134 cmp r0, #15
 *   0 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e65c0; the literal pool and
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

extern u8 native_data5_02218d90[];
extern u8 native_data_0220d114[];
extern void native_fn_02027400(void);
extern void native_fn_020414b0(void);
extern void native_fn_02041898(void);
extern void native_fn_020414c8(void);
extern void native_fn_020418b0(void);
extern void native_fn_02008c58(void);
extern void native_fn_0203cb2c(void);
extern void native_fn_0203cb64(void);
extern void native_fn_021e69a4(void);
extern void native_fn_021e6a58(void);
extern void native_fn_021e7198(void);
extern void native_fn_021e9cdc(void);
extern void native_fn_020848d0(void);
extern u8 native_data_0220d308[];
extern void native_fn_0205db90(void);
extern void native_fn_0205d9e8(void);
extern u8 native_data_0220d314[];
extern void native_fn_0205df8c(void);
extern void native_fn_0205e644(void);
extern void native_fn_0205f5dc(void);
extern void native_fn_0205f5f4(void);
extern void native_fn_021e9368(void);


asm u32 native_ov006_021e65c0 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #36
    ldr r1, =native_data5_02218d90
    mov r3, #0
    ldr r0, =native_data_0220d114
    mov r2, #127
    str r3, [r1, #0x34]
    strb r2, [r0]
    bl native_fn_02027400
    cmp r0, #9
    moveq r4, #3
    movne r4, #2
    mov r0, #63
    bl native_fn_020414b0
    mov r0, r4
    bl native_fn_02041898
    mov r0, #63
    bl native_fn_020414c8
    mov r0, r4
    bl native_fn_020418b0
    mov r0, #0
    mov r1, #102760448
    mov r2, #131072
    bl native_fn_02008c58
    mov r0, #0
    mov r1, #106954752
    mov r2, #131072
    bl native_fn_02008c58
    ldr r1, =0x05000400
    mov r0, #0
    mov r2, #1024
    bl native_fn_02008c58
    ldr r1, =0x07000400
    mov r0, #0
    mov r2, #1024
    bl native_fn_02008c58
    bl native_fn_0203cb2c
    bl native_fn_0203cb64
    bl native_fn_021e69a4
    bl native_fn_021e6a58
    bl native_fn_021e7198
    bl native_fn_021e9cdc
    bl native_fn_020848d0
    ldr r1, =native_data_0220d308
    add r0, sp, #4
    mvn r2, #0
    bl native_fn_0205db90
    mov r0, #9
    str r0, [sp]
    ldr r2, =0x020daf0c
    ldr r3, =0x020daef8
    mov r0, #1
    add r1, sp, #4
    bl native_fn_0205d9e8
    ldr r2, =native_data5_02218d90
    ldr r1, =native_data_0220d314
    str r0, [r2, #0x54]
    add r0, sp, #4
    mvn r2, #0
    bl native_fn_0205db90
    mov r0, #16
    str r0, [sp]
    ldr r2, =0x020dc368
    ldr r3, =0x020dc348
    mov r0, #1
    add r1, sp, #4
    bl native_fn_0205d9e8
    ldr r1, =native_data5_02218d90
    str r0, [r1, #0x18]
    bl native_fn_0205df8c
    ldr r0, =native_data5_02218d90
    mov r1, #0
    str r1, [r0, #0x40]
    str r1, [r0, #0xc]
    str r1, [r0, #0x24]
    str r1, [r0, #0x8]
    bl native_fn_02027400
    cmp r0, #15
    addeq sp, sp, #36
    ldmeqia sp!, {r3, r4, pc}
    bl native_fn_0205e644
    bl native_fn_0205f5dc
    ldr r1, =native_data5_02218d90
    str r0, [r1, #0x2c]
    str r0, [r1]
    bl native_fn_0205f5f4
    bl native_fn_021e9368
    add sp, sp, #36
    ldmia sp!, {r3, r4, pc}
}
