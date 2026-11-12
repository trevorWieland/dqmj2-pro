/* ov000 row 0x021edf44: 152 bytes.
 *
 * What it does: 38 instructions; 13 call(s) to 0x021edf94, 0x021ed63c, 0x02062b0c, +10 more; loops (back edge at +0x14); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x10 -> +0x50
 *   branch +0x24 -> +0x90
 *   branch +0x50 -> +0x90
 *   test +0x0c cmp r5, #0
 *   test +0x20 cmp r0, r4
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021edf44; the literal pool and
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

extern void native_fn_021ed63c(void);
extern void native_fn_02062b0c(void);
extern void native_fn_020630e4(void);
extern void native_fn_02062b34(void);
extern void native_fn_021efa14(void);
extern void native_fn_02065d88(void);


asm u32 native_ov000_021edf44 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r5, r1
    mov r6, r0
    cmp r5, #0
    ble ov000_021edf44_L50
    bl native_fn_021ed63c
    mul r4, r5, r0
    bl native_fn_02062b0c
    cmp r0, r4
    blt ov000_021edf44_L90
    mov r0, r6
    mov r1, r5
    bl native_fn_020630e4
    rsb r0, r4, #0
    bl native_fn_02062b34
    bl native_fn_02062b0c
    mov r1, #0
    bl native_fn_021efa14
    mov r0, #1
    ldmia sp!, {r4, r5, r6, pc}
ov000_021edf44_L50:
    bge ov000_021edf44_L90
    bl native_fn_02065d88
    ldr r1, [r0, #0x4]
    mvn r0, #0
    mul r1, r5, r1
    mul r4, r1, r0
    mov r0, r6
    mov r1, r5
    bl native_fn_020630e4
    mov r0, r4
    bl native_fn_02062b34
    bl native_fn_02062b0c
    mov r1, #0
    bl native_fn_021efa14
    mov r0, #1
    ldmia sp!, {r4, r5, r6, pc}
ov000_021edf44_L90:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
