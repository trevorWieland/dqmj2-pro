/* ov000 row 0x021fb250: 192 bytes.
 *
 * What it does: Writes 4 blocks of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   back edge +0x2c -> +0x20
 *   branch +0x84 -> +0x9c
 *   back edge +0xb4 -> +0x58
 *   test +0x40 cmp r8, #255
 *   test +0x80 cmp r0, #0
 *   test +0x9c cmp r0, #0
 *   test +0xb0 cmp r8, #255
 *   0 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fb250; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021fb8a8(void);
extern void native_fn_021fbc9c(void);
extern void native_fn_021fb97c(void);
extern void native_fn_021fb058(void);


asm u32 native_ov000_021fb250 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    sub sp, sp, #312
    mov r0, #0
    add r5, sp, #0
    mov r1, r0
    mov r2, r0
    mov r3, r0
    mov r4, #9
ov000_021fb250_L20:
    stmia r5!, {r0, r1, r2, r3}
    stmia r5!, {r0, r1, r2, r3}
    subs r4, r4, #1
    bne ov000_021fb250_L20
    stmia r5!, {r0, r1, r2, r3}
    stmia r5, {r0, r1}
    bl native_fn_021fb8a8
    mov r8, r0
    cmp r8, #255
    addeq sp, sp, #312
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    mov r4, #54
    add r7, sp, #0
    mov r5, #55
ov000_021fb250_L58:
    mov r0, r7
    bl native_fn_021fbc9c
    and r0, r8, #255
    bl native_fn_021fb97c
    mov r6, r0
    mov r0, r5
    mov r1, r7
    mov r2, r8
    mov r3, r6
    bl native_fn_021fb058
    cmp r0, #0
    bne ov000_021fb250_L9c
    mov r0, r4
    mov r1, r7
    mov r2, r8
    mov r3, r6
    bl native_fn_021fb058
ov000_021fb250_L9c:
    cmp r0, #0
    addeq sp, sp, #312
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    bl native_fn_021fb8a8
    mov r8, r0
    cmp r8, #255
    bne ov000_021fb250_L58
    add sp, sp, #312
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
