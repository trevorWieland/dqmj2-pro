/* ov000 row 0x0220ceb4: 220 bytes.
 *
 * What it does: 55 instructions; 9 call(s) to 0x0220cbe0, 0x02209c68, 0x0220ce54, +6 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x14 -> +0x58
 *   branch +0x24 -> +0x34
 *   branch +0x30 -> +0x58
 *   branch +0x60 -> +0xd4
 *   branch +0x7c -> +0xd4
 *   branch +0xb8 -> +0xc8
 *   branch +0xc4 -> +0xd0
 *   test +0x10 cmp r1, #0
 *   test +0x1c cmp r0, #0
 *   test +0x5c cmp r0, #10
 *   test +0x78 cmp r0, #0
 *   test +0xb0 cmp r0, #6
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220ceb4; the literal pool and
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

extern void native_fn_0220cbe0(void);
extern void native_fn_02209c68(void);
extern void native_fn_0220ce54(void);
extern void native_fn_0203d294(void);
extern void native_fn_0220a2a4(void);
extern void native_fn_02042104(void);
extern void native_fn_020c56b4(void);


asm u32 native_ov000_0220ceb4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    ldrb r1, [r5, #0x279]
    mov r4, #0
    cmp r1, #0
    bne ov000_0220ceb4_L58
    bl native_fn_0220cbe0
    cmp r0, #0
    mov r0, r5
    bne ov000_0220ceb4_L34
    mov r1, #6
    bl native_fn_02209c68
    b ov000_0220ceb4_L58
ov000_0220ceb4_L34:
    bl native_fn_0220ce54
    mvn r0, #-2147483648
    bl native_fn_0203d294
    and r0, r0, #31
    add r1, r0, #60
    add r0, r5, #512
    strh r1, [r0, #122]
    mov r0, #10
    strb r0, [r5, #0x279]
ov000_0220ceb4_L58:
    ldrb r0, [r5, #0x279]
    cmp r0, #10
    bne ov000_0220ceb4_Ld4
    add r0, r5, #512
    ldrsh r1, [r0, #122]
    sub r1, r1, #1
    strh r1, [r0, #122]
    ldrsh r0, [r0, #122]
    cmp r0, #0
    bgt ov000_0220ceb4_Ld4
    mov r1, #0
    mov r0, r5
    mov r2, r1
    bl native_fn_0220a2a4
    mov r0, r5
    mov r1, #737280
    mov r2, #0
    bl native_fn_02042104
    add r0, r5, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldrb r0, [r0, #0x7]
    cmp r0, #6
    mov r0, r5
    bne ov000_0220ceb4_Lc8
    mov r1, #7
    bl native_fn_02209c68
    b ov000_0220ceb4_Ld0
ov000_0220ceb4_Lc8:
    mov r1, #3
    bl native_fn_02209c68
ov000_0220ceb4_Ld0:
    mov r4, #1
ov000_0220ceb4_Ld4:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
