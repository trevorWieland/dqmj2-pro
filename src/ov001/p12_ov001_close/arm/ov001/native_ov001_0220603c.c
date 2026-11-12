/* ov001 row 0x0220603c: 320 bytes.
 *
 * What it does: 80 instructions; 14 call(s) to 0x0205f98c, 0x022023a8, 0x02048a60, +11 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: loop with 14 calls (80 instructions, 14 calls, 1 branch, 12 back edges, 0 literal slots).
 *
 *   branch +0x70 -> +0xd8
 *   back edge +0xd4 -> +0x74
 *   test +0x6c tst r0, #255
 *   test +0xcc cmp r4, r0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220603c; the literal pool and
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

extern void native_fn_0205f98c(void);
extern void native_fn_022023a8(void);
extern void native_fn_02048a60(void);
extern void native_fn_02048a94(void);
extern void native_fn_02048a9c(void);
extern void native_fn_0202a37c(void);
extern void native_fn_02008c14(void);
extern void native_fn_02206550(void);
extern void native_fn_022065f0(void);


asm u32 native_ov001_0220603c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r6, r0
    ldr r0, [r6, #0x1c]
    mov r1, #0
    bl native_fn_0205f98c
    mov r1, #159
    mov r5, r0
    bl native_fn_022023a8
    ldrsh r1, [r6, #20]
    ldrsh r2, [r6, #22]
    mov r0, r5
    bl native_fn_02048a60
    ldrb r1, [r6, #0x20]
    mov r0, r5
    bl native_fn_02048a94
    ldrb r1, [r6, #0x21]
    mov r0, r5
    bl native_fn_02048a9c
    ldr r0, [r5, #0x7c]
    mov r4, #0
    orr r0, r0, #2
    str r0, [r5, #0x7c]
    ldrsh r1, [r6, #20]
    ldrb r0, [r6, #0x22]
    sub r1, r1, #76
    and r5, r1, #255
    sub r0, r0, #1
    tst r0, #255
    beq ov001_0220603c_Ld8
ov001_0220603c_L74:
    add r1, r4, #1
    ldr r0, [r6, #0x1c]
    and r1, r1, #255
    bl native_fn_0205f98c
    ldrsh r2, [r6, #22]
    mov r1, r5
    mov r7, r0
    bl native_fn_02048a60
    ldrb r1, [r6, #0x20]
    mov r0, r7
    sub r1, r1, #1
    and r1, r1, #255
    bl native_fn_02048a94
    ldrb r1, [r6, #0x21]
    mov r0, r7
    bl native_fn_02048a9c
    ldrb r0, [r6, #0x22]
    add r1, r4, #1
    add r2, r5, #8
    sub r0, r0, #1
    and r4, r1, #255
    and r0, r0, #255
    cmp r4, r0
    and r5, r2, #255
    blo ov001_0220603c_L74
ov001_0220603c_Ld8:
    mov r1, #4
    mov r2, r1
    mov r0, #2
    bl native_fn_0202a37c
    mov r4, r0
    str r0, [r6, #0x40]
    mov r1, r4
    mov r0, #0
    mov r2, #4
    bl native_fn_02008c14
    ldr r1, [r6, #0x30]
    ldr r2, [r6, #0x38]
    mov r0, r6
    mov r3, #1
    bl native_fn_02206550
    ldrb r1, [r4]
    mov r0, r6
    strb r1, [r4, #0x1]
    bl native_fn_022065f0
    mvn r0, #0
    strh r0, [r6, #38]
    mov r0, #2
    str r0, [r6, #0x3c]
    mov r0, #1
    strb r0, [r6, #0x23]
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
