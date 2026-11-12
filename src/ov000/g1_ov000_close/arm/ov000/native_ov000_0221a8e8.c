/* ov000 row 0x0221a8e8: 252 bytes.
 *
 * What it does: 60 instructions; 17 call(s) to 0x0203cc3c, 0x02006b7c, 0x0203cc3c, +14 more; loops (back edge at +0x2c); returns through pop {r4, r5, r6, r7, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xf0 -> native_data_0222fae0 (image word 0x0222fae0)
 *   pool +0xf4 -> native_data_0222faf4 (image word 0x0222faf4)
 *   pool +0xf8 -> native_data_0222fb08 (image word 0x0222fb08)
 *   back edge +0x2c -> +0x14
 *   branch +0x48 -> +0x74
 *   back edge +0x70 -> +0x58
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221a8e8; the literal pool and
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

extern u8 native_data_0222fae0[];
extern void native_fn_0203cc3c(void);
extern u8 native_data_0222faf4[];
extern void native_fn_02006b7c(void);
extern void native_fn_0204518c(void);
extern void native_fn_0204820c(void);
extern void native_fn_02048308(void);
extern void native_fn_0202a498(void);
extern u8 native_data_0222fb08[];
extern void native_fn_0201d444(void);
extern void native_fn_0205ff80(void);
extern void native_fn_020c4938(void);
extern void native_fn_0221c6f0(void);
extern void native_fn_0207ce18(void);
extern void native_fn_0205ff9c(void);
extern void native_fn_0221d474(void);
extern void native_fn_02045680(void);


asm u32 native_ov000_0221a8e8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #44
    add r2, sp, #12
    mov r1, #8
    mov r0, #0
ov000_0221a8e8_L14:
    strb r0, [r2]
    strb r0, [r2, #0x1]
    strb r0, [r2, #0x2]
    strb r0, [r2, #0x3]
    add r2, r2, #4
    subs r1, r1, #1
    bne ov000_0221a8e8_L14
    ldr r0, =native_data_0222fae0
    mov r2, #0
    mov r1, #2
    strh r2, [sp]
    bl native_fn_0203cc3c
    movs r7, r0
    bne ov000_0221a8e8_L74
    ldr r5, =native_data_0222faf4
    mov r6, #1
    mov r4, #2
ov000_0221a8e8_L58:
    mov r0, r6
    bl native_fn_02006b7c
    mov r0, r5
    mov r1, r4
    bl native_fn_0203cc3c
    movs r7, r0
    beq ov000_0221a8e8_L58
ov000_0221a8e8_L74:
    add r0, sp, #4
    mov r1, r7
    mov r2, #0
    bl native_fn_0204518c
    ldr r0, [sp, #0x4]
    ldr r2, [sp, #0x8]
    mov r1, #0
    bl native_fn_0204820c
    add r0, sp, #0
    mov r1, #0
    mov r2, #2
    bl native_fn_0204820c
    bl native_fn_02048308
    mov r1, r7
    mov r0, #2
    bl native_fn_0202a498
    ldr r1, =native_data_0222fb08
    add r0, sp, #12
    bl native_fn_0201d444
    add r0, sp, #12
    bl native_fn_0205ff80
    bl native_fn_020c4938
    bl native_fn_0221c6f0
    bl native_fn_020c4938
    bl native_fn_0207ce18
    bl native_fn_0205ff9c
    bl native_fn_0221d474
    mov r0, #2
    bl native_fn_02045680
    add sp, sp, #44
    ldmia sp!, {r4, r5, r6, r7, pc}
}
