//@version=5
strategy("Just want to make trading simple", overlay=true)

// EMA Slope + EMA Cross Strategy
MA1_Length = input(2, title="EMA 1 Length")
MA2_Length = input(4, title="EMA 2 Length")
MA3_Length = input(20, title="EMA 3 Length")

price = close
MA1 = ta.ema(price, MA1_Length)
MA2 = ta.ema(price, MA2_Length)
MA3 = ta.ema(price, MA3_Length)

long = ta.crossunder(price, MA3) or (ta.change(price) < 0 and ta.change(MA1) < 0 and ta.crossunder(price, MA1) and ta.change(MA2) > 0)
short = ta.crossover(price, MA3) or (ta.change(price) > 0 and ta.change(MA1) > 0 and ta.crossover(price, MA1) and ta.change(MA2) < 0) 

// Entry and Exit Conditions for the Strategy
strategy.entry("Long", strategy.long, when=long)
strategy.close("Long", when=short) // Exit long position when short condition is met

strategy.entry("Short", strategy.short, when=short)
strategy.close("Short", when=long) // Exit short position when long condition is met

// Alert Conditions for the Strategy
alertcondition(long, title='EMA Slope + EMA Cross Strategy, Long Alert', message='Go Long!')
alertcondition(short, title='EMA Slope + EMA Cross Strategy, Short Alert', message='Go Short!')

// Indicator: Supertrend (ATR Length 10, Factor 0.4) - Updated factor to 0.4
atrPeriod1 = input(10, "ATR Length")
factor1 = input.float(0.4, "Factor 1", step=0.01) // Updated factor to 0.4

[supertrend1, direction1] = ta.supertrend(factor1, atrPeriod1)

bodyMiddle = plot((open + close) / 2, display=display.none)
upTrend1 = plot(direction1 < 0 ? supertrend1 : na, "Up Trend 1", color=color.green, style=plot.style_linebr)
downTrend1 = plot(direction1 < 0 ? supertrend1 : na, "Down Trend 1", color=color.red, style=plot.style_linebr)

fill(bodyMiddle, upTrend1, color.new(color.green, 90), fillgaps=false)
fill(bodyMiddle, downTrend1, color.new(color.red, 90), fillgaps=false)

// Indicator: Supertrend (ATR Length 10, Factor 0.8) - Updated factor to 0.8
atrPeriod2 = input(10, "ATR Length")
factor2 = input.float(0.8, "Factor 2", step=0.01) // Updated factor to 0.8

[supertrend2, direction2] = ta.supertrend(factor2, atrPeriod2)

upTrend2 = plot(direction2 < 0 ? supertrend2 : na, "Up Trend 2", color=color.blue, style=plot.style_linebr)
downTrend2 = plot(direction2 < 0 ? supertrend2 : na, "Down Trend 2", color=color.orange, style=plot.style_linebr)

fill(bodyMiddle, upTrend2, color.new(color.blue, 90), fillgaps=false)
fill(bodyMiddle, downTrend2, color.new(color.orange, 90), fillgaps=false)

// Indicator: Moving Averages
switch2 = input(true, title="Show Moving Averages?")
MA2_color = ta.change(MA2) > 0 ? color.lime : ta.change(MA2) < 0 ? color.red : color.blue
MA3_color = ta.change(MA3) > 0 ? color.lime : ta.change(MA3) < 0 ? color.red : color.blue

plot(switch2 ? MA2 : na, title="EMA 2", style=plot.style_linebr, linewidth=2, color=MA2_color)
plot(switch2 ? MA3 : na, title="EMA 3", style=plot.style_linebr, linewidth=4, color=MA3_color)

// Bar Colors
bar_color = long ? color.new(color.green, 80) : short ? color.new(color.red, 80) : na
bar_color2 = long ? color.new(color.blue, 80) : short ? color.new(color.orange, 80) : na
bar_color_combined = bar_color != na ? bar_color : bar_color2
barcolor(bar_color_combined)








# MA AGNLE INDICATOR

//@version=4
// this indicator gives you the angles of different moving averages
// this can give an indication of the momentum of a move increasing or decreasing
// you can also set a threshold for a minimum angle to filter out "no trade" zones

// JD.
// #NotTradingAdvice #DYOR

study("ma angles - JD")
src = input(ohlc4, title="source")
th = input(2, minval=1, title="threshold for -no trade zones- in degrees")
color_bars = input(false, title="color bars?")
no_trade = input(false, title="black out bars in no trade zones?")

// definition of "Jurik Moving Average", by Everget
jma(_src, _length, _phase, _power) =>
    phaseRatio = _phase < -100 ? 0.5 : _phase > 100 ? 2.5 : _phase / 100 + 1.5
    beta = 0.45 * (_length - 1) / (0.45 * (_length - 1) + 2)
    alpha = pow(beta, _power)
    jma = 0.0
    e0 = 0.0
    e0 := (1 - alpha) * _src + alpha * nz(e0[1])
    e1 = 0.0
    e1 := (_src - e0) * (1 - beta) + beta * nz(e1[1])
    e2 = 0.0
    e2 := (e0 + phaseRatio * e1 - nz(jma[1])) * pow(1 - alpha, 2) + 
       pow(alpha, 2) * nz(e2[1])
    jma := e2 + nz(jma[1])
    jma

//// //// Determine Angle by KyJ //// //// 
angle(_src) =>
    rad2degree = 180 / 3.14159265359  //pi 
    ang = rad2degree * atan((_src[0] - _src[1]) / atr(14))
    ang

jma_line = jma(src, 10, 50, 1)
jma_line_fast = jma(src, 10, 50, 2)
ma27 = ema(src, 27)
ma83 = ema(src, 83)
ma278 = ema(src, 278)
jma_slope = angle(jma_line)
jma_fast_slope = angle(jma_line_fast)
ma27_slope = angle(ma27)
ma83_slope = angle(ma83)
ma278_slope = angle(ma278)

hline(0)
rising_1 = rising(ma27, 1)
color_1 = color.new(color.green, 75)
falling_1 = falling(ma27, 1)
plot(jma_slope, title="jma slope", style=plot.style_area, color=jma_slope >= 0 ? rising_1 ? color.green : color_1 : falling_1 ? color.red : color.maroon)
plot(jma_fast_slope, title="jma slope", style=plot.style_line, color=jma_fast_slope >= 0 ? color.green : color.red, transp=0)
plot(ma27_slope, title="ma27 slope filter", style=plot.style_area, color=abs(ma27_slope) > th ? na : color.yellow)
plot(ma83_slope, title="ma83 slope filter", style=plot.style_area, color=abs(ma83_slope) > th ? na : color.yellow)
plot(ma278_slope, title="ma278 slope filter", style=plot.style_area, color=abs(ma278_slope) > th ? na : color.yellow)
plot(ma27_slope, title="ma27 slope", style=plot.style_line, linewidth=2, color=ma27_slope >= 0 ? color.lime : color.fuchsia)
color_2 = color.new(color.green, 0)
color_3 = color.new(color.red, 0)
plot(ma83_slope, title="ma83 slope", style=plot.style_line, color=ma83_slope >= 0 ? color_2 : color_3)
plot(ma278_slope, title="ma278 slope", style=plot.style_line, color=ma278_slope >= 0 ? color.green : color.red)

plotshape(ma27_slope >= 0 ? ma27 : na, style=shape.triangleup, location=location.bottom, color=color.green)
plotshape(ma27_slope < 0 ? ma27 : na, style=shape.triangledown, location=location.top, color=color.red)
plotshape(ma27_slope >= 0 and not(ma27_slope[1] >= 0) ? ma27 : na, style=shape.triangleup, location=location.bottom, size=size.tiny, color=color.green)
plotshape(ma27_slope < 0 and not(ma27_slope[1] < 0) ? ma27 : na, style=shape.triangledown, location=location.top, size=size.tiny, color=color.red)
rising_2 = rising(ma27, 1)
falling_2 = falling(ma27, 1)
barcolor(color_bars ? no_trade and abs(ma27_slope) <= th ? color.white : jma_slope >= 0 ? rising_2 ? color.lime : color.green : falling_2 ? color.fuchsia : color.red : na)