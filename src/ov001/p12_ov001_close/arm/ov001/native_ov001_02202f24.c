/* ov001 row 0x02202f24: 116 bytes.
 *
 * What it does: 29 instructions; 5 call(s) to 0x0220b74c, 0x0220b770, 0x0220b794, +2 more; loops (back edge at +0x28); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 5 calls (29 instructions, 5 calls, 2 branches, 2 back edges, 0 literal slots).
 *
 *   branch +0x4c -> +0x5c
 *   back edge +0x6c -> +0x44
 *   test +0x1c cmp r5, #0
 *   test +0x34 cmp r7, #0
 *   test +0x44 cmp r4, #4
 *   test +0x48 cmpne r4, r5
 *   test +0x64 cmp r7, r0, asr #24
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02202f24; the literal pool and
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

extern void native_fn_0220b74c(void);
extern void native_fn_0220b770(void);
extern void native_fn_0220b794(void);
extern void native_fn_021db530(void);
extern void native_fn_0220473c(void);


asm u32 native_ov001_02202f24 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    bl native_fn_0220b74c
    mov r6, r0
    bl native_fn_0220b770
    mov r5, r0
    bl native_fn_0220b794
    mov r4, r0
    cmp r5, #0
    ldmeqia sp!, {r3, r4, r5, r6, r7, pc}
    mov r0, r6
    bl native_fn_021db530
    mov r7, r0
    mov r5, #0
    cmp r7, #0
    ldmleia sp!, {r3, r4, r5, r6, r7, pc}
    mov r0, r6, lsl #24
    mov r6, r0, asr #24
ov001_02202f24_L44:
    cmp r4, #4
    cmpne r4, r5
    bne ov001_02202f24_L5c
    mov r0, r6
    mov r1, r5
    bl native_fn_0220473c
ov001_02202f24_L5c:
    add r0, r5, #1
    mov r0, r0, lsl #24
    cmp r7, r0, asr #24
    mov r5, r0, asr #24
    bgt ov001_02202f24_L44
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
