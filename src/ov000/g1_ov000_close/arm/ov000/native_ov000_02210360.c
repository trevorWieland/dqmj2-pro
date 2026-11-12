/* ov000 row 0x02210360: 392 bytes.
 *
 * What it does: 94 instructions; 19 call(s) to 0x021e0e04, 0x022104d0, 0x022103d0, +16 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, r7, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block load.
 *
 *   pool +0x178 -> constant 0x022385b8 (image word 0x022385b8)
 *   pool +0x17c -> constant 0x022385d4 (image word 0x022385d4)
 *   pool +0x180 -> constant 0x022385ec (image word 0x022385ec)
 *   pool +0x184 -> constant 0x00271000 (image word 0x00271000)
 *   branch +0x10 -> +0x170
 *   branch +0x20 -> +0x170
 *   branch +0x3c -> +0x70
 *   back edge +0x6c -> +0x44
 *   branch +0x8c -> +0x170
 *   branch +0xac -> +0xb8
 *   branch +0x108 -> +0x118
 *   branch +0x138 -> +0x144
 *   test +0x0c cmp r0, #0
 *   test +0x1c cmp lr, #0
 *   test +0x28 cmp lr, #1
 *   test +0x64 cmp r3, lr
 *   test +0xb0 cmp r4, #127
 *   test +0xfc cmp r0, r1
 *   test +0x10c cmp r0, #368640
 *   test +0x130 cmp r6, r0
 *   test +0x13c cmp r6, #127
 *   1 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02210360; the literal pool and
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

extern void native_fn_021e0e04(void);
extern void native_fn_0200236c(void);
extern void native_fn_02002480(void);
extern void native_fn_021d8a50(void);
extern void native_fn_0202818c(void);
extern void native_fn_021d8aa0(void);
extern void native_fn_02028158(void);
extern void native_fn_021dfdc4(void);
extern void native_fn_021e7b9c(void);
extern void native_fn_021e7bbc(void);
extern void native_fn_0205f76c(void);


asm u32 native_ov000_02210360 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r4, #0
    bl native_fn_021e0e04
    cmp r0, #0
    beq ov000_02210360_L170
    ldr r0, =0x022385b8
    ldrsb lr, [r0, #1]
    cmp lr, #0
    ble ov000_02210360_L170
    ldr r0, =0x022385d4
    cmp lr, #1
    ldr r7, [r0]
    ldr r6, [r0, #0x4]
    mov r5, r4
    mov r3, #1
    ble ov000_02210360_L70
    ldr r12, =0x022385ec
ov000_02210360_L44:
    ldr r2, [r12]
    ldr r1, [r12, #0x4]
    subs r0, r2, r7
    sbcs r0, r1, r6
    movlt r5, r3
    add r3, r3, #1
    movlt r7, r2
    movlt r6, r1
    cmp r3, lr
    add r12, r12, #24
    blt ov000_02210360_L44
ov000_02210360_L70:
    ldr r2, =0x022385d4
    mov r0, #24
    mla r5, r0, r5, r2
    ldr r1, =0x00271000
    ldmia r5, {r0, r2}
    subs r1, r0, r1
    sbcs r1, r2, #0
    bge ov000_02210360_L170
    bl native_fn_0200236c
    mov r1, r0, lsl #5
    add r0, r1, r0, lsl #7
    mov r1, #102400
    bl native_fn_02002480
    rsbs r4, r0, #160
    movmi r4, #0
    bmi ov000_02210360_Lb8
    cmp r4, #127
    movgt r4, #127
ov000_02210360_Lb8:
    mov r0, #0
    bl native_fn_021d8a50
    add r1, r5, #8
    bl native_fn_0202818c
    mov r7, r0
    mov r0, #0
    bl native_fn_021d8a50
    mov r6, r0
    mov r0, #0
    bl native_fn_021d8aa0
    mov r1, r0
    mov r0, r6
    bl native_fn_0202818c
    sub r0, r0, r7
    bl native_fn_02028158
    mov r1, #368640
    rsb r1, r1, #0
    cmp r0, r1
    sublt r1, r1, r0
    addlt r0, r0, r1
    blt ov000_02210360_L118
    cmp r0, #368640
    subgt r1, r0, #368640
    subgt r0, r0, r1
ov000_02210360_L118:
    add r0, r0, #368640
    mov r0, r0, lsl #8
    mov r1, #737280
    bl native_fn_02002480
    sub r6, r0, #127
    mvn r0, #127
    cmp r6, r0
    movlt r6, r0
    blt ov000_02210360_L144
    cmp r6, #127
    movgt r6, #127
ov000_02210360_L144:
    ldr r0, [r5, #0x14]
    add r0, r0, #13
    bl native_fn_021dfdc4
    bl native_fn_021e7b9c
    mov r5, r0
    mov r1, r4
    bl native_fn_021e7bbc
    mov r0, r5
    mov r1, r6
    bl native_fn_0205f76c
    mov r4, #1
ov000_02210360_L170:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
