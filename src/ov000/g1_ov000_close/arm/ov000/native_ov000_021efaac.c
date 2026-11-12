/* ov000 row 0x021efaac: 292 bytes.
 *
 * What it does: 71 instructions; 5 call(s) to 0x021efb28, 0x0205e7a8, 0x02049ad0, +2 more; loops (back edge at +0x84); 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x11c -> constant 0x02236c1c (image word 0x02236c1c)
 *   pool +0x120 -> native_data_0222ee80 (image word 0x0222ee80)
 *   branch +0x24 -> +0x88
 *   branch +0x34 -> +0x78
 *   branch +0x60 -> +0x7c
 *   branch +0x74 -> +0x7c
 *   test +0x20 cmp r1, #0
 *   test +0x30 cmp r1, r3
 *   test +0x48 cmp r2, #0
 *   test +0x54 cmp r1, r0
 *   test +0x90 cmp r0, #0
 *   test +0x104 cmp r1, r0
 *   3 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021efaac; the literal pool and
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

extern void native_fn_0205e7a8(void);
extern u8 native_data_0222ee80[];
extern void native_fn_02049ad0(void);
extern void native_fn_0204a010(void);
extern void native_fn_0204a154(void);


asm u32 native_ov000_021efaac (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #12
    ldr r0, =0x02236c1c
    add r3, sp, #8
    ldr r1, [r0, #0x8]
    mov r2, #0
    strh r2, [r3]
    strh r2, [r3, #2]
    cmp r1, #0
    beq ov000_021efaac_L88
    ldr r3, [r0, #0x14]
    ldr r1, [r0, #0xc]
    cmp r1, r3
    beq ov000_021efaac_L78
    ldr r0, =0x02236c1c
    subs r1, r1, r3
    ldr r2, [r0, #0x10]
    rsbmi r1, r1, #0
    cmp r2, #0
    movge r0, r2
    rsblt r0, r2, #0
    cmp r1, r0
    ldrle r0, =0x02236c1c
    strle r3, [r0, #0xc]
    ble ov000_021efaac_L7c
    ldr r0, =0x02236c1c
    ldr r1, [r0, #0xc]
    add r1, r1, r2
    str r1, [r0, #0xc]
    b ov000_021efaac_L7c
ov000_021efaac_L78:
    str r2, [r0, #0x8]
ov000_021efaac_L7c:
    mvn r0, #0
    mov r1, #95
    bl native_fn_0205e7a8
ov000_021efaac_L88:
    ldr r0, =native_data_0222ee80
    ldr r0, [r0]
    cmp r0, #0
    addeq sp, sp, #12
    ldmeqia sp!, {pc}
    mov r0, #16
    bl native_fn_02049ad0
    mov r1, #16
    str r1, [sp]
    ldr r0, [r0]
    mov r1, #32
    ldr r0, [r0, #0x4]
    mov r2, #0
    mov r3, #48
    bl native_fn_0204a010
    ldr r0, =0x02236c1c
    mov r3, #6
    ldrsh r12, [r0, #4]
    mov r2, #0
    add r1, sp, #8
    rsb r12, r12, #32
    strh r12, [sp, #8]
    str r3, [sp]
    str r2, [sp, #0x4]
    ldr r3, [r0, #0xc]
    mov r0, #16
    mov r2, #1
    bl native_fn_0204a154
    ldr r0, =0x02236c1c
    ldr r1, [r0, #0xc]
    ldr r0, [r0, #0x14]
    cmp r1, r0
    ldreq r0, =native_data_0222ee80
    moveq r1, #0
    streq r1, [r0]
    add sp, sp, #12
    ldmia sp!, {pc}
}
