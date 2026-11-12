/* ov000 row 0x02211830: 304 bytes.
 *
 * What it does: 75 instructions; 17 call(s) to 0x02211944, 0x02211578, 0x02211644, +14 more; loops (back edge at +0x34); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x12c -> constant 0x0224157c (image word 0x0224157c)
 *   branch +0x2c -> +0x114
 *   branch +0x3c -> +0x110
 *   branch +0x48 -> +0x64
 *   branch +0x60 -> +0x84
 *   branch +0x74 -> +0x84
 *   branch +0x8c -> +0x9c
 *   branch +0x98 -> +0xbc
 *   branch +0xac -> +0xbc
 *   branch +0xcc -> +0xdc
 *   back edge +0x120 -> +0x24
 *   test +0x28 cmp r0, #0
 *   test +0x38 cmp r0, #0
 *   test +0x44 cmp r1, #0
 *   test +0x70 cmp r0, #0
 *   test +0x88 cmp r1, #0
 *   test +0xa8 cmp r0, #0
 *   test +0xc8 cmp r0, #0
 *   test +0x118 cmp r8, #24
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02211830; the literal pool and
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

extern void native_fn_02211578(void);
extern void native_fn_02211644(void);
extern void native_fn_02211774(void);
extern void native_fn_021dfb6c(void);
extern void native_fn_022116ac(void);
extern void native_fn_021dfc3c(void);
extern void native_fn_021dfcd8(void);
extern void native_fn_02211710(void);
extern void native_fn_022117b8(void);
extern void native_fn_02029870(void);


asm u32 native_ov000_02211830 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r9, #0
    ldr r10, =0x0224157c
    mov r8, r9
    mov r11, r9
    mov r6, r9
    mvn r7, #0
    mov r5, #1
    mov r4, #9
ov000_02211830_L24:
    ldrsh r0, [r10]
    cmp r0, #0
    ble ov000_02211830_L114
    mov r0, r10
    bl native_fn_02211578
    cmp r0, #0
    beq ov000_02211830_L110
    ldrb r1, [r10, #0x7]
    cmp r1, #0
    beq ov000_02211830_L64
    mov r0, r10
    bl native_fn_02211644
    mov r0, r10
    mov r1, r7
    bl native_fn_02211774
    b ov000_02211830_L84
ov000_02211830_L64:
    ldrsh r0, [r10]
    mov r1, r6
    bl native_fn_021dfb6c
    cmp r0, #0
    ble ov000_02211830_L84
    mov r0, r10
    mov r1, r11
    bl native_fn_02211644
ov000_02211830_L84:
    ldrb r1, [r10, #0x8]
    cmp r1, #0
    beq ov000_02211830_L9c
    mov r0, r10
    bl native_fn_022116ac
    b ov000_02211830_Lbc
ov000_02211830_L9c:
    ldrsh r0, [r10]
    mov r1, #0
    bl native_fn_021dfc3c
    cmp r0, #0
    ble ov000_02211830_Lbc
    mov r0, r10
    mov r1, #0
    bl native_fn_022116ac
ov000_02211830_Lbc:
    ldrsh r0, [r10]
    mov r1, #0
    bl native_fn_021dfcd8
    cmp r0, #0
    ble ov000_02211830_Ldc
    mov r0, r10
    mov r1, #0
    bl native_fn_02211710
ov000_02211830_Ldc:
    mov r0, r10
    bl native_fn_022117b8
    ldr r1, [r10, #0x114]
    add r0, r10, #20
    str r1, [r10, #0x84]
    ldr r2, [r10, #0x118]
    add r1, r10, #288
    str r2, [r10, #0x88]
    ldr r2, [r10, #0x11c]
    str r2, [r10, #0x8c]
    bl native_fn_02029870
    strb r5, [r10, #0xa]
    add r9, r9, #1
ov000_02211830_L110:
    strb r4, [r10, #0x1f]
ov000_02211830_L114:
    add r8, r8, #1
    cmp r8, #24
    add r10, r10, #360
    blt ov000_02211830_L24
    mov r0, r9
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
