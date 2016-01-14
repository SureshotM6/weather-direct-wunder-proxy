# Registration request #
no data in request

# Weather request #
```
send link quality 0x64
send battery status
model/unit? 

63 24 03 b3
   14


Rx

00.11 ? version?

city name with A=0x01, 16 characters

BCD hour
BCD min
BCD sec
BCD day
BCD month
BCD year

0x0000

BCD sunrise hour/minute
BCD sunset hour/minute

temperatures are +40
days contain 10 bytes

high t
low t
12/13 - didn't change anything
27.27.22.22.22 (overall?)
  00 = INVALID
  01 = clear skies (sun icon)
  02 = mostly clear
  03 = mostly cloudy
  04 = overcast
  05 = clear skies (wind icon only)
  06 = clear skies (wind+sun icon)
  07 = mostly clear with chance of light rain
  08 = mostly clear with chance of heavy rain
  09 = overcast with chance of light rain
  0a = overcast with chance of heavy rain
  0b = mostly cloudy with chance of light rain and t-storms
  0c = mostly cloudy with chance of rain shows and t-storms
  0d = mostly clear with chance of light rain and t-storms
  0e = mostly clear with chance of light snow and freezing rain
  0f = mostly clear with chance of light snow
  10 = mostly clear with chance of snow
  11 = mostly cloudy with chance of light rain snow mix
  12 = mostly cloudy with chance of light snow
  13 = mostly cloudy with chance of heavy snow
  14 = BAD - clear skies (BAD - have snow and t-storm icon)
  15 = partly cloudy with chance of heavy snow and thunder
  16 = mostly clear with chance of light rain snow mix
  17 = partly cloudy with chance of light freezing rain
  18 = mostly clear with chance of light freezing rain or sleet with thunder
  19 = overcast with chance of light rain snow mix with thunder
  1a = mostly cloudy with chance of freezing rain or sleet
  1b = mostly cloudy with chance of freezing rain with thunder
  1c = INVALID
  
  1d = INVALID
  1e = INVALID
  1f = INVALID
  20 = INVALID
  
  21 = clear skies
  22 = partly cloudy
  23 = mostly cloudy
  24 = overcast
  
  25 = clear skies (just wind icon)
  26 = clear skies (sun+wind icon)
  27 = partly cloudy with chance of light rain
  28 = mostly cloudy with chance of heavy rain
  
  29 = overcast with chance of rain showers
  2a = overcast with chance of heavy rain
  2b = cloudy with chance of light rain and t-storms
  2c = cloudy with chance of rain showers and t-storms
  
  2d = partly cloudy with chance of light rain and t-storms
  2e = partly cloudy with chance of light snow and freezing rain
  2f = partly cloudy with chance of light snow 
  30 = partly cloudy with chance of snow
  
  31 = mostly cloudy with chance of rain snow mix
  32 = mostly cloudy with chance of snow
  33 = overcase with chance of heavy snow
  34 = clear skies (BAD - snow and t-storm icon)
  
  35 = mostly cloudy with chance of heavy snow and thunder
  36 = partly cloudy with chance of light rain snow mix
  37 = partly cloudy with chance of freezing rain
  38 = partly cloudy with chance of light freezing rain or sleet with thunder 
  
  39 = overcast with chance of rain snow mix with thunder
  3a = overcast with chance of light freezing rain or sleet
  3b = overcast with hance of light freezing rain with thunder
  3c = INVALID
  
  3d = INVALID
  3e = INVALID
  3f = INVALID
  40 = INVALID

06.06.06.05.07
01.01.02.02.02
A1.D1.41.70.92
29
80.83.88.91.90
c2.72.41.33.32

checksum for all prior bytes +7


morning/afternoon/evening/night for 5 day forecast (20 total) - starts at 0x51:

... 20 fields of 7 ...

(checksum + 7)

pad with aa to 256 bytes
```