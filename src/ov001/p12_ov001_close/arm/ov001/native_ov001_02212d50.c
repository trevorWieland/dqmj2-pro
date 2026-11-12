/* ov001 row 0x02212d50: 452 bytes.
 *
 * What it does: 113 instructions; 24 call(s) to 0x0205f98c, 0x02048a60, 0x02048a94, +21 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}
 *
 * Decoded shape: loop with 24 calls (113 instructions, 24 calls, 0 branches, 24 back edges, 0 literal slots).
 *
 *   back edge +0x64 -> +0x10
 *   back edge +0xcc -> +0x88
 *   test +0x60 cmp r7, #24
 *   test +0xc4 cmp r5, #27
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02212d50; the literal pool and
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

extern void native_fn_0205f98c(void);
extern void native_fn_02048a60(void);
extern void native_fn_02048a94(void);
extern void native_fn_02048a9c(void);
extern void native_fn_022129f4(void);
extern void native_fn_0202a37c(void);


asm u32 native_ov001_02212d50 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    mov r6, r0
    mov r7, #0
    mov r4, #7
ov001_02212d50_L10:
    ldr r0, [r6, #0x1c]
    and r1, r7, #255
    bl native_fn_0205f98c
    ldrsh r1, [r6, #20]
    ldrsh r2, [r6, #22]
    mov r5, r0
    bl native_fn_02048a60
    mov r0, r5
    mov r1, r4
    bl native_fn_02048a94
    ldrb r1, [r6, #0x21]
    mov r0, r5
    bl native_fn_02048a9c
    mov r0, r7, asr #1
    strh r0, [r5, #130]
    ldrsb r2, [r5, #136]
    mov r0, r6
    and r1, r7, #255
    bl native_fn_022129f4
    add r7, r7, #1
    cmp r7, #24
    blt ov001_02212d50_L10
    ldrsh r1, [r6, #20]
    ldrsh r0, [r6, #22]
    mov r5, #24
    sub r1, r1, #44
    sub r0, r0, #10
    and r9, r1, #255
    and r4, r0, #255
    mov r7, #6
ov001_02212d50_L88:
    ldr r0, [r6, #0x1c]
    and r1, r5, #255
    bl native_fn_0205f98c
    mov r8, r0
    mov r1, r9
    mov r2, r4
    bl native_fn_02048a60
    mov r0, r8
    mov r1, r7
    bl native_fn_02048a94
    ldrb r1, [r6, #0x21]
    mov r0, r8
    bl native_fn_02048a9c
    add r0, r9, #14
    add r5, r5, #1
    cmp r5, #27
    and r9, r0, #255
    blt ov001_02212d50_L88
    ldrsh r2, [r6, #20]
    ldr r0, [r6, #0x1c]
    mov r1, #28
    sub r2, r2, #2
    and r7, r2, #255
    bl native_fn_0205f98c
    mov r5, r0
    mov r1, r7
    mov r2, r4
    bl native_fn_02048a60
    mov r0, r5
    mov r1, #6
    bl native_fn_02048a94
    ldrb r1, [r6, #0x21]
    mov r0, r5
    bl native_fn_02048a9c
    ldrsh r2, [r6, #20]
    ldr r0, [r6, #0x1c]
    mov r1, #29
    add r2, r2, #4
    and r5, r2, #255
    bl native_fn_0205f98c
    mov r1, r5
    mov r5, r0
    mov r2, r4
    bl native_fn_02048a60
    mov r0, r5
    mov r1, #6
    bl native_fn_02048a94
    ldrb r1, [r6, #0x21]
    mov r0, r5
    bl native_fn_02048a9c
    ldrsh r2, [r6, #20]
    ldr r0, [r6, #0x1c]
    mov r1, #27
    add r2, r2, #16
    and r5, r2, #255
    bl native_fn_0205f98c
    mov r2, r4
    mov r1, r5
    mov r4, r0
    bl native_fn_02048a60
    mov r0, r4
    mov r1, #6
    bl native_fn_02048a94
    ldrb r1, [r6, #0x21]
    mov r0, r4
    bl native_fn_02048a9c
    mov r0, #1
    str r0, [r6, #0x2c]
    mov r1, #0
    str r1, [r6, #0x38]
    mov r1, #40
    mov r2, #4
    bl native_fn_0202a37c
    str r0, [r6, #0x40]
    ldr r2, [r6, #0x30]
    mov r1, #0
    str r2, [r0, #0x20]
    str r1, [r6, #0x44]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
