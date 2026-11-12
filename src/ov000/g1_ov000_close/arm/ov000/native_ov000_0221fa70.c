/* ov000 row 0x0221fa70: 328 bytes.
 *
 * What it does: 81 instructions; 12 call(s) to 0x0221d05c, 0x0221d05c, 0x0221d05c, +9 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x144 -> constant 0x022463b0 (image word 0x022463b0)
 *   back edge +0x84 -> +0x54
 *   branch +0xb0 -> +0xe4
 *   back edge +0xe0 -> +0xb8
 *   branch +0xf0 -> +0x118
 *   back edge +0x114 -> +0xf8
 *   test +0x80 cmp r4, #6
 *   test +0x90 cmp r0, #0
 *   test +0xac cmp r0, #0
 *   test +0xc8 cmp r0, r6
 *   test +0xdc cmp r5, r0
 *   test +0xe4 cmp r4, #0
 *   test +0xec cmp r4, #6
 *   test +0x110 cmp r4, #6
 *   test +0x138 cmp r0, #0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221fa70; the literal pool and
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

extern void native_fn_0221d05c(void);
extern void native_fn_02049ad0(void);
extern void native_fn_0221f6e8(void);


asm u32 native_ov000_0221fa70 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r2, =0x022463b0
    mov r5, r0
    mov r0, #16
    str r1, [r2, #0x28]
    bl native_fn_0221d05c
    ldr r1, =0x022463b0
    mov r0, #17
    ldr r1, [r1, #0x28]
    bl native_fn_0221d05c
    ldr r1, =0x022463b0
    mov r0, #18
    ldr r1, [r1, #0x28]
    bl native_fn_0221d05c
    ldr r1, =0x022463b0
    mov r0, #19
    ldr r1, [r1, #0x28]
    bl native_fn_0221d05c
    ldr r6, =0x022463b0
    mov r4, #0
    mov r7, #1
ov000_0221fa70_L54:
    add r0, r4, #20
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    strb r7, [r0, #0x5]
    add r0, r4, #20
    mov r0, r0, lsl #24
    ldr r1, [r6, #0x28]
    mov r0, r0, asr #24
    bl native_fn_0221d05c
    add r4, r4, #1
    cmp r4, #6
    blt ov000_0221fa70_L54
    ldr r7, =0x022463b0
    ldr r0, [r7, #0x28]
    cmp r0, #0
    ldmeqia sp!, {r3, r4, r5, r6, r7, pc}
    ldr r0, [r5]
    mov r4, #0
    str r0, [r7, #0xc]
    ldr r0, [r7, #0x10]
    mov r5, r4
    cmp r0, #0
    ble ov000_0221fa70_Le4
    mvn r6, #0
ov000_0221fa70_Lb8:
    ldr r1, [r7, #0xc]
    mov r0, r5
    and r1, r1, #255
    bl native_fn_0221f6e8
    cmp r0, r6
    addne r0, r4, #1
    andne r4, r0, #255
    ldr r0, [r7, #0x10]
    add r5, r5, #1
    cmp r5, r0
    blt ov000_0221fa70_Lb8
ov000_0221fa70_Le4:
    cmp r4, #0
    moveq r4, #1
    cmp r4, #6
    bge ov000_0221fa70_L118
    mov r5, #127
ov000_0221fa70_Lf8:
    add r0, r4, #20
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02049ad0
    add r4, r4, #1
    strb r5, [r0, #0x5]
    cmp r4, #6
    blt ov000_0221fa70_Lf8
ov000_0221fa70_L118:
    ldr r1, =0x022463b0
    mov r4, #1
    strb r4, [r1, #0x1]
    ldr r3, [r1, #0x1c]
    ldr r2, [r1, #0xc]
    mov r0, #132
    mla r0, r2, r0, r3
    ldr r0, [r0, #0x14]
    cmp r0, #0
    strneb r4, [r1, #0x4]
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
