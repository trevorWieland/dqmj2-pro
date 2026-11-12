/* ov000 row 0x021f50e8: 236 bytes.
 *
 * What it does: 58 instructions; 12 call(s) to 0x02061944, 0x020622ec, 0x02065d28, +9 more; loops (back edge at +0x08); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xe8 -> native_data_0222b986 (image word 0x0222b986)
 *   back edge +0x50 -> +0x28
 *   back edge +0xdc -> +0xc4
 *   test +0x4c cmp r6, #12
 *   test +0xd8 cmp r4, #36
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f50e8; the literal pool and
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
extern void native_fn_020622ec(void);
extern u8 native_data_0222b986[];
extern void native_fn_02065d28(void);
extern void native_fn_0206dec8(void);
extern void native_fn_02061250(void);
extern void native_fn_02045dc4(void);
extern void native_fn_02062144(void);
extern void native_fn_02061dcc(void);


asm u32 native_ov000_021f50e8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #8
    bl native_fn_02061944
    mov r4, r0
    mov r0, #6
    mov r1, #12
    mov r2, #0
    bl native_fn_020622ec
    ldr r5, =native_data_0222b986
    mov r6, #0
ov000_021f50e8_L28:
    mov r0, r6, lsl #1
    ldrsb r0, [r5, r0]
    bl native_fn_02065d28
    add r1, r6, #1
    ldr r2, [r4, #0x25c]
    mov r1, r1, lsl #24
    sub r0, r2, r0
    mov r6, r1, asr #24
    str r0, [r4, #0x25c]
    cmp r6, #12
    blt ov000_021f50e8_L28
    bl native_fn_0206dec8
    mov r0, #0
    bl native_fn_02061250
    mov r2, #5
    mov r1, r0
    str r2, [sp]
    mov r12, #15
    mov r0, #0
    mov r2, #1
    mov r3, #8
    str r12, [sp, #0x4]
    bl native_fn_02045dc4
    mov r0, #1
    bl native_fn_02061250
    mov r1, r0
    mov r0, #5
    str r0, [sp]
    mov r0, #15
    str r0, [sp, #0x4]
    mov r0, #0
    mov r2, #1
    mov r3, #8
    bl native_fn_02045dc4
    add r0, r4, #512
    ldrsb r0, [r0, #111]
    mov r1, #0
    bl native_fn_02062144
    mov r4, #0
ov000_021f50e8_Lc4:
    mov r0, r4
    bl native_fn_02061dcc
    add r0, r4, #1
    mov r0, r0, lsl #24
    mov r4, r0, asr #24
    cmp r4, #36
    blt ov000_021f50e8_Lc4
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, pc}
}
