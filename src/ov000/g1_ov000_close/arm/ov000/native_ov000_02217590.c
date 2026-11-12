/* ov000 row 0x02217590: 228 bytes.
 *
 * What it does: 57 instructions; 13 call(s) to 0x02062aa0, 0x02062ad0, 0x02063b18, +10 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x30 -> +0xdc
 *   branch +0x44 -> +0xd4
 *   branch +0x4c -> +0x5c
 *   branch +0x58 -> +0x64
 *   branch +0x6c -> +0xc4
 *   branch +0x98 -> +0xbc
 *   branch +0xb8 -> +0xc4
 *   branch +0xc0 -> +0xd4
 *   back edge +0xd0 -> +0x48
 *   test +0x24 cmp r0, #0
 *   test +0x2c cmp r7, #0
 *   test +0x40 cmp r8, #0
 *   test +0x48 cmp r7, r6
 *   test +0x68 cmp r9, #0
 *   test +0x94 cmp r10, r0
 *   test +0xb4 cmp r10, r0
 *   test +0xcc cmp r7, r8
 *   test +0xd4 cmp r11, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02217590; the literal pool and
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

extern void native_fn_02062aa0(void);
extern void native_fn_02062ad0(void);
extern void native_fn_02063b18(void);
extern void native_fn_02062a50(void);
extern void native_fn_02062a88(void);
extern void native_fn_02215d94(void);
extern void native_fn_02210f94(void);
extern void native_fn_02210f74(void);
extern void native_fn_02210f9c(void);
extern void native_fn_02210f84(void);


asm u32 native_ov000_02217590 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r7, r0
    mov r5, #1
    bl native_fn_02062aa0
    mov r6, r0
    bl native_fn_02062ad0
    mov r4, r0
    mov r0, #61
    bl native_fn_02063b18
    cmp r0, #0
    moveq r5, #0
    cmp r7, #0
    beq ov000_02217590_Ldc
    add r8, r6, r4
    mov r11, #0
    mov r7, r11
    cmp r8, #0
    ble ov000_02217590_Ld4
ov000_02217590_L48:
    cmp r7, r6
    bge ov000_02217590_L5c
    mov r0, r7
    bl native_fn_02062a50
    b ov000_02217590_L64
ov000_02217590_L5c:
    sub r0, r7, r6
    bl native_fn_02062a88
ov000_02217590_L64:
    mov r9, r0
    cmp r9, #0
    beq ov000_02217590_Lc4
    mov r0, r7
    bl native_fn_02215d94
    mov r4, r0
    mov r0, r9
    bl native_fn_02210f94
    mov r10, r0
    mov r0, r9
    mov r1, r4
    bl native_fn_02210f74
    cmp r10, r0
    blt ov000_02217590_Lbc
    mov r0, r9
    bl native_fn_02210f9c
    mov r10, r0
    mov r0, r9
    mov r1, r4
    bl native_fn_02210f84
    cmp r10, r0
    bge ov000_02217590_Lc4
ov000_02217590_Lbc:
    mov r11, #1
    b ov000_02217590_Ld4
ov000_02217590_Lc4:
    add r0, r7, #1
    and r7, r0, #255
    cmp r7, r8
    blt ov000_02217590_L48
ov000_02217590_Ld4:
    cmp r11, #0
    moveq r5, #0
ov000_02217590_Ldc:
    mov r0, r5
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
