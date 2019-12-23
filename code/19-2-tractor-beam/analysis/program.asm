00000: add base, 424

00002: in [base+1]
; check non-negative
00004: add [base+0], 11, 0
00008: jnz 1, 282
; abs
00011: mul [base+0], 1, 18
00015: jnz 1, 259

00018: mul [221], 1, [base+1]
00022: in [base+1]
; check non-negative
00024: mul [base+0], 1, 31
00028: jnz 1, 282
; abs
00031: mul [base+0], 38, 1
00035: jnz 1, 259

; TBD-1
00038: add [base+2], 0, [23]
00042: mul [base+3], 1, [base+1]
00046: add [base+1], 1, 0
00050: add [base+0], 57, 0
00054: jnz 1, 303

00057: add [222], 0, [base+1]

; abs (X, X, 259)
00061: mul [base+3], [221], 1
00065: mul [base+2], [221], 1
00069: mul [base+1], 1, 259
00073: add [base+0], 0, 80
00077: jnz 1, 225

00080: mul [base+2], 83, 1
00084: mul [base+0], 1, 91
00088: jz 0, 303

00091: add [223], 0, [base+1]

00095: mul [base+4], 1, [222]
00099: add [base+3], 0, 259
00103: add [base+2], 0, 225
00107: add [base+1], 225, 0
00111: add [base+0], 118, 0
00115: jz 0, 225

00118: add [base+3], 0, [222]
00122: add [base+2], 34, 0
00126: add [base+0], 133, 0
00130: jnz 1, 303

00133: mul [base+1], [base+1], -1
00137: add [base+1], [223], [base+1]
00141: mul [base+0], 1, 148
00145: jz 0, 259

00148: add [223], [base+1], 0
00152: mul [base+4], 1, [221]
00156: add [base+3], 0, [222]
00160: add [base+2], 12, 0
00164: add [224], [132], -2
00168: mul [224], [224], 2
00172: add [224], [224], 3
00176: mul [132], [132], -1
00180: add [224], [224], [132]
00184: add [base+1], [224], 1
00188: add [base+0], 195, 0
00192: jnz 1, [108]

00195: mov [base+2], [base+1] < [223]
00199: add [base+1], 0, [23]
00203: mul [base+3], 1, -1
00207: mul [base+0], 214, 1
00211: jnz 1, 303

00214: add [base+1], 1, [base+1]
00218: out [base+1]
00220: hlt

00221: dw 0, 0, 0, 0

00225: add base, 5
00227: mul [249], [base-4], 1  ; mutates jnz at 0247
00231: add [base+1], 0, [base-3]
00235: add [base+2], 0, [base-2]
00239: add [base+3], [base-1], 0
00243: add [base+0], 0, 250
00247: jnz 1, 225
00250: add [base-4], [base+1], 0
00254: add base, -5
00256: jz 0, [base+0]

; abs
00259: add base, 3
00261: mov [base-1], 0 < [base-2]
00265: mul [base-1], [base-1], 2
00269: add [base-1], [base-1], -1
00273: mul [base-2], [base-1], [base-2]
00277: add base, -3
00279: jz 0, [base+0]

; check non-negative input
00282: add base, 3
00284: mov [base-1], [base-2] < 0
00288: jz [base-1], 294
00291: out 0
00293: hlt

00294: add [base-2], 0, [base-2]
00298: add base, -3
00300: jz 0, [base+0]

; TBD: A, x, B, x, 0
00303: add base, 5
00305: mov [base-1], [base-3] < [base-4]
00309: jz [base-1], 346
00312: add [base-4], [base-4], [base-3]
00316: mul [base-1], [base-3], -1
00320: add [base+2], [base-4], [base-1]
00324: mul [base-1], [base+2], -1
00328: add [base+1], [base-4], [base-1]
00332: add [base+3], [base-2], 0
00336: add [base+0], 343, 0
00340: jnz 1, 303

00343: jnz 1, 415

00346: mov [base-1], [base-2] < [base-3]
00350: jz [base-1], 387
00353: add [base-3], [base-3], [base-2]
00357: mul [base-1], [base-2], -1
00361: add [base+3], [base-3], [base-1]
00365: mul [base-1], [base+3], -1
00369: add [base+2], [base-3], [base-1]
00373: add [base+1], [base-4], 0
00377: add [base+0], 384, 0
00381: jnz 1, 303

00384: jz 0, 415

00387: mul [base-4], [base-4], -1
00391: add [base-4], [base-4], [base-3]
00395: mul [base-2], [base-3], [base-2]
00399: mul [base-4], [base-2], [base-4]
00403: mul [base-3], [base-3], [base-2]
00407: mul [base-2], [base-4], -1
00411: add [base+1], [base-3], [base-2]

00415: mul [base-4], [base+1], 1
00419: add base, -5
00421: jz 0, [base+0]
