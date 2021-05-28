; General flow:
; Gcode for stage (move to pos)
; fire command
; Some kind of trigger for images
; some kind of trigger for spectra
; assert data has been collected
; Next shot

; set to mm and absolute reference
G21 G90
; set current pos as home
g92 x0 y0
; Go to first firing position
G01 x10 y10
;fire
FIRE
; within fire, data is collected and asserted,
; and code will not fire again until code knows data is collected