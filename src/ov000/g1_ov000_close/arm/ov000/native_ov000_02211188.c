/* ov000 row 0x02211188: 136 bytes.
 *
 * What it does: 34 instructions; 3 call(s) to 0x02211148, 0x02008d78, 0x021df950; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}
 *
 * Decoded shape: chunk loop.
 *
 *   branch +0x20 -> +0x80
 *   4 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02211188; the literal pool and
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

extern void native_fn_02211148(void);
extern void native_fn_02008d78(void);
extern void native_fn_021df950(void);


asm u32 native_ov000_02211188 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    mov r4, r0
    mov r9, r1
    mov r8, r2
    mov r7, r3
    mov r6, #0
    bl native_fn_02211148
    movs r5, r0
    beq ov000_02211188_L80
    strh r4, [r5]
    add r3, r5, #276
    ldmia r9, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    add r3, r5, #288
    ldmia r8, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    strh r7, [r5, #2]
    mov r3, #1
    strb r3, [r5, #0x9]
    mov r0, r6
    strb r0, [r5, #0xa]
    strb r0, [r5, #0xb]
    add r0, r5, #336
    mov r1, #255
    mov r2, #20
    strb r3, [r5, #0xc]
    bl native_fn_02008d78
    mov r1, r6
    mov r0, r4
    str r1, [r5, #0x164]
    bl native_fn_021df950
    mov r6, #1
ov000_02211188_L80:
    mov r0, r6
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
