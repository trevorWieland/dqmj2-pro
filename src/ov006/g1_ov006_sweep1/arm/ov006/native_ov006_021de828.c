/* ov006 row 0x021de828: 200 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xc0 -> native_data_02207940 (image word 0x02207940)
 *   pool +0xc4 -> native_data2_0220f594 (image word 0x0220f594)
 *   test +0x24 cmp r0, #1
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021de828; the literal pool and
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

extern u8 native_data_02207940[];
extern u8 native_data2_0220f594[];
extern void native_fn_0204a644(void);
extern void native_fn_021df134(void);
extern void native_fn_02049604(void);
extern void native_fn_02049ad0(void);
extern void native_fn_021dddc4(void);
extern void native_fn_021ddf44(void);
extern void native_fn_0206006c(void);


asm u32 native_ov006_021de828 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #16
    ldr r1, =native_data_02207940
    ldr r0, =native_data2_0220f594
    ldrh r2, [r1, #26]
    ldrh r1, [r1, #24]
    ldr r0, [r0, #0x1c]
    strh r2, [sp, #14]
    strh r1, [sp, #12]
    cmp r0, #1
    add r1, sp, #12
    addeq sp, sp, #16
    ldmeqia sp!, {r4, pc}
    mov r0, #8
    strh r0, [sp, #12]
    mov r0, #4
    str r0, [sp]
    mov r4, #1
    str r4, [sp, #0x4]
    mov r0, #31
    mov r2, #5
    mov r3, #2
    str r4, [sp, #0x8]
    bl native_fn_0204a644
    bl native_fn_021df134
    mov r1, r4
    bl native_fn_02049604
    mov r0, #31
    bl native_fn_02049ad0
    mov r4, r0
    ldrsb r0, [r4, #5]
    bl native_fn_021dddc4
    ldr r1, [r4]
    mov r0, r0, lsl #24
    ldr r4, [r1, #0x4]
    mov r0, r0, asr #24
    bl native_fn_021ddf44
    ldrsb r1, [r4, #31]
    str r1, [sp]
    ldrsb r1, [r4, #28]
    ldrsb r2, [r4, #29]
    ldrsb r3, [r4, #30]
    bl native_fn_0206006c
    ldr r0, =native_data2_0220f594
    mov r1, #1
    str r1, [r0, #0x1c]
    add sp, sp, #16
    ldmia sp!, {r4, pc}
}
