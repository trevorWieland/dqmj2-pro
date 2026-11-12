/* ov001 row 0x02200144: 168 bytes.
 *
 * What it does: 40 instructions; 8 call(s) to 0x02202360, 0x02041814, 0x021db438, +5 more; loops (back edge at +0x14); returns through pop {r4, r5, r6, r7, r8, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 8 calls (40 instructions, 8 calls, 0 branches, 3 back edges, 2 literal slots).
 *
 *   pool +0xa0 -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0xa4 -> constant 0x02239de0 (image word 0x02239de0)
 *   test +0x18 cmp r0, #1
 *   test +0x28 cmp r7, #0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02200144; the literal pool and
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

extern void native_fn_02202360(void);
extern void native_fn_02041814(void);
extern void native_fn_021db438(void);
extern void native_fn_02207938(void);
extern void native_fn_022042c4(void);
extern void native_fn_02202b88(void);
extern void native_fn_021fd074(void);
extern void native_fn_02207944(void);


asm u32 native_ov001_02200144 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #12]
    bl native_fn_02202360
    mov r6, r0
    bl native_fn_02041814
    cmp r0, #1
    moveq r0, #0
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    ldrb r7, [r6, #0x14]
    cmp r7, #0
    ldreqsb r8, [r6, #8]
    mov r0, r7
    ldrnesb r8, [r6, #10]
    mov r1, r8
    bl native_fn_021db438
    mov r5, r0
    bl native_fn_02207938
    mov r4, r0
    add r0, r6, #168
    bl native_fn_022042c4
    bl native_fn_02202b88
    str r5, [r4, #0x10]
    str r7, [r4, #0x24]
    str r8, [r4, #0x28]
    ldr r0, [r4, #0x24]
    mov r1, r8, lsl #24
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r1, asr #24
    bl native_fn_021fd074
    ldr r1, =0x02239de0
    str r0, [r4, #0x538]
    ldr r0, [r1, #0x30]
    bl native_fn_02207944
    ldr r0, =0x02239c10
    mov r1, #13
    strb r1, [r0, #0xa]
    mov r0, #1
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
