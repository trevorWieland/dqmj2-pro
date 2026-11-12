/* ov000 row 0x022055f0: 188 bytes.
 *
 * What it does: 47 instructions; 9 call(s) to 0x02061944, 0x0206ea80, 0x022056d8, +6 more; loops (back edge at +0x04); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x24 -> +0x34
 *   branch +0x2c -> +0x44
 *   branch +0x30 -> +0xb4
 *   branch +0x4c -> +0xa4
 *   back edge +0x98 -> +0x68
 *   test +0x20 cmp r1, #0
 *   test +0x28 cmp r1, #1
 *   test +0x48 cmp r0, #0
 *   test +0x94 cmp r7, #5
 *   test +0xac cmp r0, #42
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022055f0; the literal pool and
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
extern void native_fn_0206ea80(void);
extern void native_fn_022056d8(void);
extern void native_fn_02062328(void);
extern void native_fn_02062144(void);
extern void native_fn_02061dcc(void);
extern void native_fn_02049f4c(void);
extern void native_fn_022057a8(void);


asm u32 native_ov000_022055f0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    bl native_fn_02061944
    mov r4, r0
    bl native_fn_0206ea80
    add r1, r4, #512
    ldrsb r1, [r1, #106]
    mov r5, r0
    mov r6, #0
    cmp r1, #0
    beq ov000_022055f0_L34
    cmp r1, #1
    beq ov000_022055f0_L44
    b ov000_022055f0_Lb4
ov000_022055f0_L34:
    bl native_fn_022056d8
    mov r0, #1
    strb r0, [r4, #0x26a]
    strb r0, [r5, #0xc]
ov000_022055f0_L44:
    ldrsb r0, [r5, #12]
    cmp r0, #0
    beq ov000_022055f0_La4
    bl native_fn_02062328
    add r0, r4, #512
    ldrsb r0, [r0, #111]
    mov r1, #0
    bl native_fn_02062144
    mov r7, #0
ov000_022055f0_L68:
    add r0, r7, #6
    mov r0, r0, lsl #24
    mov r8, r0, asr #24
    mov r0, r8
    bl native_fn_02061dcc
    bl native_fn_02049f4c
    mov r0, r8
    bl native_fn_022057a8
    add r0, r7, #1
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    cmp r7, #5
    blt ov000_022055f0_L68
    mov r0, #0
    strb r0, [r5, #0xc]
ov000_022055f0_La4:
    add r0, r4, #512
    ldrsb r0, [r0, #108]
    cmp r0, #42
    movne r6, #1
ov000_022055f0_Lb4:
    mov r0, r6
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
