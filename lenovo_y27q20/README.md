# [Lenovo Y27q-20](https://support.lenovo.com/us/en/solutions/pd500310-lenovo-y27q-20-monitor-overview)

## Video Gain (Drive): API to OSD
This table maps numbers read from the VESA MCCS API to numbers shown on the OSD (on-screen display) for the red, green, and blue video gain drive channels. As you can see, the two data sources do not line up. The API's minimum and maximum values are both out of range for the OSD, yet when you use the API to set values beyond the OSD's range, it continues to under/overdrive the matching color channel. (Note: This was made by manipulating the API and observing the OSD. The code uses simple [linear interpolation](https://calculator-online.net/linear-interpolation-calculator/) with rounding and boundaries, but I'm keeping the entire data set here for future reference.)

| API | OSD |
| --- | --- |
| 0...11 | 0 |
| 12 | 2 |
| 13 | 5 |
| 14 | 7 |
| 15 | 10 |
| 16 | 13 |
| 17 | 15 |
| 18 | 18 |
| 19 | 20 |
| 20 | 23 |
| 21 | 25 |
| 22 | 28 |
| 23 | 30 |
| 24 | 33 |
| 25 | 35 |
| 26 | 38 |
| 27 | 40 |
| 28 | 43 |
| 29 | 46 |
| 30 | 48 |
| 31 | 51 |
| 32 | 53 |
| 33 | 56 |
| 34 | 58 |
| 35 | 61 |
| 36 | 63 |
| 37 | 66 |
| 38 | 68 |
| 39 | 71 |
| 40 | 74 |
| 41 | 76 |
| 42 | 79 |
| 43 | 81 |
| 44 | 84 |
| 45 | 86 |
| 46 | 89 |
| 47 | 91 |
| 48 | 94 |
| 49 | 96 |
| 50 | 99 |
| 51...100 | 100 |

## Video Gain (Drive): OSD to API
This table maps numbers shown on the OSD (on-screen display) to numbers read from the VESA MCCS API for the red, green, and blue video gain drive channels. (Note: This was made by manipulating the OSD and observing the API. It is *not* a simple inversion of the API-to-OSD mapping, and some values don't appear to line up between the two mappings presumably due to rounding.)

| OSD | API |
| --- | --- |
| 0...1 | 11 |
| 2...3 | 12 |
| 4...6 | 13 |
| 7...8 | 14 |
| 9...11 | 15 |
| 12...13 | 16 |
| 14...16 | 17 |
| 17...18 | 18 |
| 19...21 | 19 |
| 22...24 | 20 |
| 25...26 | 21 |
| 27...29 | 22 |
| 30...31 | 23 |
| 32...34 | 24 |
| 35...36 | 25 |
| 37...39 | 26 |
| 40...41 | 27 |
| 42...44 | 28 |
| 45...46 | 29 |
| 47...49 | 30 |
| 50...52 | 31 |
| 53...54 | 32 |
| 55...57 | 33 |
| 58...59 | 34 |
| 60...62 | 35 |
| 63...64 | 36 |
| 65...67 | 37 |
| 68...69 | 38 |
| 70...72 | 39 |
| 73...74 | 40 |
| 75...77 | 41 |
| 78...79 | 42 |
| 80...82 | 43 |
| 83...85 | 44 |
| 86...87 | 45 |
| 88...90 | 46 |
| 91...92 | 47 |
| 93...95 | 48 |
| 96...97 | 49 |
| 98...100 | 50 |
