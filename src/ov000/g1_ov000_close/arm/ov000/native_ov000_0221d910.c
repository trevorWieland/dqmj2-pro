/* ov000 row 0x0221d910: 300 bytes.
 *
 * What it does: 74 instructions; 12 call(s) to 0x02068bd4, 0x02062a50, 0x020692b0, +9 more; loops (back edge at +0x14); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x128 -> constant 0x02246318 (image word 0x02246318)
 *   branch +0x38 -> +0x6c
 *   back edge +0x74 -> +0x2c
 *   branch +0x9c -> +0xd0
 *   back edge +0xd8 -> +0x90
 *   test +0x70 cmp r4, #3
 *   test +0xd4 cmp r10, #3
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221d910; the literal pool and
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

extern void native_fn_02068bd4(void);
extern void native_fn_02062a50(void);
extern void native_fn_020692b0(void);
extern void native_fn_02044cdc(void);
extern void native_fn_02062a88(void);
extern void native_fn_020bfb10(void);
extern void native_fn_02068c14(void);


asm u32 native_ov000_0221d910 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    ldr r1, =0x02246318
    mov r11, r0
    ldr r0, [r1, #0x10]
    bl native_fn_02068bd4
    mov r5, #0
    mov r4, r5
    mov r8, r5
    mov r7, #12
    mov r6, #15
ov000_0221d910_L2c:
    mov r0, r4
    bl native_fn_02062a50
    movs r9, r0
    beq ov000_0221d910_L6c
    str r8, [sp]
    str r7, [sp, #0x4]
    str r6, [sp, #0x8]
    ldr r0, [r9, #0x14]
    mov r1, r8
    mov r2, r8
    and r3, r5, #255
    bl native_fn_020692b0
    ldrsh r0, [r9, #24]
    bl native_fn_02044cdc
    add r0, r0, #1
    add r5, r5, r0
ov000_0221d910_L6c:
    add r4, r4, #1
    cmp r4, #3
    blt ov000_0221d910_L2c
    mov r9, #0
    mov r10, r9
    mov r7, r9
    mov r6, #12
    mov r5, #15
    mov r4, #1
ov000_0221d910_L90:
    mov r0, r10
    bl native_fn_02062a88
    movs r8, r0
    beq ov000_0221d910_Ld0
    str r7, [sp]
    str r6, [sp, #0x4]
    str r5, [sp, #0x8]
    ldr r0, [r8, #0x14]
    mov r1, r4
    mov r2, r7
    and r3, r9, #255
    bl native_fn_020692b0
    ldrsh r0, [r8, #24]
    bl native_fn_02044cdc
    add r0, r0, #1
    add r9, r9, r0
ov000_0221d910_Ld0:
    add r10, r10, #1
    cmp r10, #3
    blt ov000_0221d910_L90
    mov r0, r11
    bl native_fn_020bfb10
    mov r1, #0
    str r1, [sp]
    mov r4, #12
    mov r0, r11
    mov r2, r1
    mov r3, r1
    str r4, [sp, #0x4]
    mov r4, #15
    str r4, [sp, #0x8]
    bl native_fn_020692b0
    mov r0, #2
    mov r1, #36
    mov r2, #32
    mov r3, #1
    bl native_fn_02068c14
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
