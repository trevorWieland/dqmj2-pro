/* ov000 row 0x021f520c: 252 bytes.
 *
 * What it does: 61 instructions; 10 call(s) to 0x02061944, 0x0201d444, 0x0205ff80, +7 more; loops (back edge at +0x08); returns through pop {r4, r5, r6, r7, r8, r9, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xf4 -> native_data_0222f2d4 (image word 0x0222f2d4)
 *   pool +0xf8 -> native_data_0222b986 (image word 0x0222b986)
 *   back edge +0x7c -> +0x38
 *   branch +0xb0 -> +0xd8
 *   back edge +0xe8 -> +0x98
 *   test +0x78 cmp r8, #12
 *   test +0xe4 cmp r8, #3
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f520c; the literal pool and
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

extern void native_fn_02061944(void);
extern u8 native_data_0222f2d4[];
extern void native_fn_0201d444(void);
extern void native_fn_0205ff80(void);
extern u8 native_data_0222b986[];
extern void native_fn_02065730(void);
extern void native_fn_0205ff9c(void);
extern void native_fn_020624c0(void);
extern void native_fn_02223d40(void);
extern void native_fn_02061de4(void);


asm u32 native_ov000_021f520c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #36
    bl native_fn_02061944
    mov r7, r0
    ldr r1, =native_data_0222f2d4
    add r0, sp, #4
    bl native_fn_0201d444
    add r0, sp, #4
    bl native_fn_0205ff80
    mov r8, #0
    ldr r5, =native_data_0222b986
    add r6, r7, #16
    mov r4, r8
    mov r9, #12
ov000_021f520c_L38:
    add r1, r8, #1
    ldr r2, [r7, #0x25c]
    mla r0, r1, r9, r6
    str r2, [sp]
    mov r1, r8, lsl #1
    add r2, r5, r8, lsl #1
    ldrsb r1, [r5, r1]
    ldrb r3, [r2, #0x1]
    mov r2, r4
    bl native_fn_02065730
    add r1, r8, #1
    ldr r2, [r7, #0x25c]
    mov r1, r1, lsl #24
    add r0, r2, r0
    mov r8, r1, asr #24
    str r0, [r7, #0x25c]
    cmp r8, #12
    blt ov000_021f520c_L38
    bl native_fn_0205ff9c
    mov r8, #0
    add r4, r7, #16
    mov r5, r8
    mov r6, #19
    mov r7, #12
ov000_021f520c_L98:
    mov r0, r6
    add r9, r8, #3
    bl native_fn_020624c0
    mov r1, r8
    bl native_fn_02223d40
    movs r1, r0
    beq ov000_021f520c_Ld8
    mla r0, r9, r7, r4
    str r5, [sp]
    ldrsh r1, [r1, #24]
    mov r2, r8
    mov r3, r5
    bl native_fn_02061de4
    add r0, r8, r0
    mov r0, r0, lsl #24
    mov r8, r0, asr #24
ov000_021f520c_Ld8:
    add r0, r8, #1
    mov r0, r0, lsl #24
    mov r8, r0, asr #24
    cmp r8, #3
    blt ov000_021f520c_L98
    add sp, sp, #36
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
}
