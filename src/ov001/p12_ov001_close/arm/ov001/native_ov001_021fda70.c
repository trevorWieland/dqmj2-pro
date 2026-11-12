/* ov001 row 0x021fda70: 180 bytes.
 *
 * What it does: 44 instructions; 8 call(s) to 0x021db530, 0x021fddb4, 0x021db438, +5 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 8 calls (44 instructions, 8 calls, 1 branch, 6 back edges, 1 literal slot).
 *
 *   pool +0xb0 -> constant 0x02239fac (image word 0x02239fac)
 *   back edge +0xa8 -> +0x28
 *   test +0x18 cmp r8, #0
 *   test +0xa0 cmp r8, r0, asr #24
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fda70; the literal pool and
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

extern void native_fn_021db530(void);
extern void native_fn_021fddb4(void);
extern void native_fn_021db438(void);
extern void native_fn_021fd074(void);
extern void native_fn_02202384(void);
extern void native_fn_02202398(void);
extern void native_fn_0206d250(void);
extern void native_fn_02065818(void);


asm u32 native_ov001_021fda70 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r0, #0
    ldr r7, =0x02239fac
    bl native_fn_021db530
    mov r8, r0
    mov r10, #0
    cmp r8, #0
    ldmleia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r6, r10
    mov r11, r10
ov001_021fda70_L28:
    mov r0, r10
    mov r1, r8
    bl native_fn_021fddb4
    mov r0, r6
    mov r1, r10
    bl native_fn_021db438
    mov r0, r11
    mov r1, r10
    bl native_fn_021fd074
    mov r5, r0
    mov r0, #0
    bl native_fn_02202384
    mov r0, r0, lsl #21
    mov r9, r0, asr #24
    mov r0, #0
    mov r1, r10
    bl native_fn_02202398
    mov r4, r0
    ldrsb r0, [r5, #12]
    bl native_fn_0206d250
    add r0, r0, r0, lsl #2
    add r0, r0, r4, asr #3
    add r0, r0, #4
    mov r0, r0, lsl #24
    mov r2, r0, asr #24
    mov r1, r9
    mov r0, r7
    bl native_fn_02065818
    add r0, r10, #1
    mov r0, r0, lsl #24
    cmp r8, r0, asr #24
    mov r10, r0, asr #24
    bgt ov001_021fda70_L28
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
