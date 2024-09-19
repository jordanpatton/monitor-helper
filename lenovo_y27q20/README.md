# [Lenovo Y27q-20](https://support.lenovo.com/us/en/solutions/pd500310-lenovo-y27q-20-monitor-overview)
This monitor has some bizarre quirks, and it's only partially compatible with [MCCS](https://en.wikipedia.org/wiki/Monitor_Control_Command_Set). The main problem is that it's incapable of storing any changes in non-volatile storage unless you use the hardware interface. (The API doesn't auto-save changes, and the `0xB0 (Settings)` code does nothing.) It will apply software-based changes temporarily, but it will revert to its prior state after the monitor sleeps or power cycles.

## Monitor Capabilities
The monitor responds to a capabilities query with the following string: `(prot(monitor)type(LCD)model(Lenovo Y27fq)cmds(01 02 03 07 0C E3 F3)vcp(02 04 05 06 08 0B 0C 10 12 14(01 02 04 05 06 08 0B) 16 18 1A 52 60(01 03 04 0F 10 11 12) 87 AC AE B2 B6 C6 C8 CA CC(01 02 03 04 06 0A 0D) D6(01 04 05) DF FD FF)mswhql(1)asset_eep(40)mccs_ver(2.2))` I have parsed this into a table below and added some information from manual testing. (You can get more information by scanning with [ddcutil](https://www.ddcutil.com).)

| Code | Description | Notes |
| ---- | ----------- | ----- |
| 0x01 |                                             |                                                                                  |
| 0x02 | New Control Value                           |                                                                                  |
| 0x03 | Soft Controls                               | Does nothing (but is listed in `cmds`).                                          |
| 0x04 | Restore Factory Defaults                    |                                                                                  |
| 0x05 | Restore Factory Luminance/Contrast Defaults |                                                                                  |
| 0x06 | Restore Factory Geometry Defaults           |                                                                                  |
| 0x07 |                                             |                                                                                  |
| 0x08 | Restore Factory Color Defaults              |                                                                                  |
| 0x0B | Color Temperature Increment                 |                                                                                  |
| 0x0C | Color Temperature Request                   |                                                                                  |
| 0x10 | Luminance                                   |                                                                                  |
| 0x12 | Contrast                                    |                                                                                  |
| 0x14 | Select Color Preset                         | API response values: 0x01, 0x02, 0x04, 0x05, 0x06, 0x08, 0x0B.                   |
| 0x16 | Video Gain (Drive): Red                     |                                                                                  |
| 0x18 | Video Gain (Drive): Green                   |                                                                                  |
| 0x1A | Video Gain (Drive): Blue                    |                                                                                  |
| 0x52 | Active Control                              | API response value range changes during use.                                     |
| 0x60 | Input Source                                | API response values: 0x01, 0x03, 0x04, 0x0F, 0x10, 0x11, 0x12.                   |
| 0x87 | Sharpness                                   |                                                                                  |
| 0xAC | Horizontal Frequency                        |                                                                                  |
| 0xAE | Vertical Frequency                          |                                                                                  |
| 0xB0 | Settings                                    | Does nothing (and is not listed in `cmds` or `vcp`).                             |
| 0xB2 | Flat Panel Sub-Pixel Layout                 |                                                                                  |
| 0xB6 | Display Technology Type                     |                                                                                  |
| 0xC6 | Display Usage Time                          |                                                                                  |
| 0xC8 | Display Controller ID                       |                                                                                  |
| 0xCA | OSD / Button Event Control                  |                                                                                  |
| 0xCC | OSD Language                                | API response values: 0x01, 0x02, 0x03, 0x04, 0x06, 0x0A, 0x0D.                   |
| 0xD6 | Power Mode                                  | API response values: 0x01, 0x04, 0x05.                                           |
| 0xDF | VCP Version                                 |                                                                                  |
| 0xE0 | Manufacturer Specific (Over Drive)          | Known values: 0=Off, 1=Normal, 2=Extreme.                                        |
| 0xE2 | Manufacturer Specific (USB charge)          | Known values: 0=Off, 1=On.                                                       |
| 0xE3 | Manufacturer Specific                       | Does nothing (but is listed in `cmds` and `vcp`).                                |
| 0xEA | Manufacturer Specific (DCR)                 | Known values: 0=Off, 1=On.                                                       |
| 0xF1 | Manufacturer Specific                       | API response values: 1...65535.                                                  |
| 0xF3 | Manufacturer Specific                       | Does nothing (but is listed in `cmds`).                                          |
| 0xFA | Manufacturer Specific (Refresh Rate Num)    | Known values: 0=Off, 1=Top Left, 2=Top Right, 3=Bottom Left, 4=Bottom Right.     |
| 0xFB | Manufacturer Specific (Game mode)           | Known values: 0=Off, 1=FPS1, 2=FPS2, 3=Racing, 4=RTS, 5=Game 1, 6=Game 2, 7=Off. |
| 0xFD | Manufacturer Specific                       | Unsupported (but is listed in `vcp`).                                            |
| 0xFF | Manufacturer Specific                       | Unsupported (but is listed in `vcp`).                                            |

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

## Lenovo Artery Data
[Lenovo Artery v2.0.3920.2](https://pcsupport.lenovo.com/us/en/downloads/DS543485) has the following JSON blob for this monitor in its configurations. The monitor is *supposed* to be [`Y27q-20`](https://support.lenovo.com/us/en/solutions/pd500310-lenovo-y27q-20-monitor-overview), but some software packages register it as `Y27fq`, so I've included everything `Y27`-related below. Lenovo Artery's changes **do not** persist through sleep or power cycle.
```json
{
  "Monitors": [
    {
      "Model": "LEN Y27gq-20 % LEN Y27gq-25 % LEN Y27q-20 %  Y27gq-20 % Y27gq-25 % Y27q-20 % Y25-25",
      "SizeX": 27,
      "Ratio": "16:9",
      "SyncType": "G-Sync",
      "OEM": "Lenovo",
      "ImgUrl": "",
      "LowBlueLightMode": {
        "Icon": "text",
        "Name": "Text",
        "Brightness": -1,
        "Contrast": -1,
        "Temperature": -1,
        "RGain": -1,
        "GGain": -1,
        "BGain": 20,
        "OpCode": {
          "Code": "0xdc",
          "Arg": "0x6"
        }
      },
      "CancelLowBlueLightMode": {
        "Icon": "text",
        "Name": "Text",
        "Brightness": -1,
        "Contrast": -1,
        "Temperature": -1,
        "RGain": -1,
        "GGain": -1,
        "BGain": 20,
        "OpCode": {
          "Code": "0xdc",
          "Arg": "0x0"
        }
      },
      "LowBlueMethod": "Scenario",
      "OEMFunctions": [],
      "ColorModes": [],
      "ScenarioModes": [],
      "InputPins": [
        {
          "type": "DP",
          "Name": "Display Port",
          "OpCode1": {
            "Code": "0x60",
            "Arg": "0x0F"
          },
          "OpCode2": {
            "Code": "0x60",
            "Arg": "0x2F"
          }
        },
        {
          "type": "HDMI",
          "Name": "HDMI1",
          "OpCode1": {
            "Code": "0x60",
            "Arg": "0x11"
          },
          "OpCode2": {
            "Code": "0x60",
            "Arg": "0x21"
          }
        },
        {
          "type": "TypeC",
          "Name": "USB C1",
          "OpCode1": {
            "Code": "0x60",
            "Arg": "0x13"
          },
          "OpCode2": {
            "Code": "0x60",
            "Arg": "0x23"
          }
        },
        {
          "type": "TypeC",
          "Name": "USB C2",
          "OpCode1": {
            "Code": "0x60",
            "Arg": "0x14"
          },
          "OpCode2": {
            "Code": "0x60",
            "Arg": "0x24"
          }
        }
      ]
    },
    {
      "Model": "Y25f % Y25g % Y27g % Y27f",
      "LowBlueLightMode": {
        "Icon": "text",
        "Name": "Text",
        "Brightness": -1,
        "Contrast": -1,
        "Temperature": -1,
        "RGain": -1,
        "GGain": -1,
        "BGain": 20,
        "OpCode": {
          "Code": "",
          "Arg": ""
        }
      },
      "CancelLowBlueLightMode": {
        "Icon": "text",
        "Name": "Text",
        "Brightness": -1,
        "Contrast": -1,
        "Temperature": -1,
        "RGain": -1,
        "GGain": -1,
        "BGain": 60,
        "OpCode": {
          "Code": "",
          "Arg": ""
        }
      },
      "ScenarioModes": [
        {
          "Icon": "text",
          "Name": "Text",
          "Brightness": 50,
          "Contrast": 50,
          "Temperature": 6500,
          "RGain": -1,
          "GGain": -1,
          "BGain": -1,
          "OpCode": {
            "Code": "",
            "Arg": ""
          }
        },
        {
          "Icon": "photo",
          "Name": "Photo",
          "Brightness": 70,
          "Contrast": 60,
          "Temperature": 6500,
          "RGain": -1,
          "GGain": -1,
          "BGain": -1,
          "OpCode": {
            "Code": "",
            "Arg": ""
          }
        },
        {
          "Icon": "game",
          "Name": "Game",
          "Brightness": 100,
          "Contrast": 50,
          "Temperature": 6500,
          "RGain": -1,
          "GGain": -1,
          "BGain": -1,
          "OpCode": {
            "Code": "",
            "Arg": ""
          }
        },
        {
          "Icon": "video",
          "Name": "Movie",
          "Brightness": 90,
          "Contrast": 65,
          "Temperature": 9300,
          "RGain": -1,
          "GGain": -1,
          "BGain": -1,
          "OpCode": {
            "Code": "",
            "Arg": ""
          }
        }
      ],
      "InputPins": [
        {
          "type": "DP",
          "Name": "Display Port",
          "OpCode1": {
            "Code": "0x60",
            "Arg": "0x0F"
          },
          "OpCode2": {
            "Code": "0x60",
            "Arg": "0x2F"
          }
        },
        {
          "type": "HDMI",
          "Name": "HDMI1",
          "OpCode1": {
            "Code": "0x60",
            "Arg": "0x11"
          },
          "OpCode2": {
            "Code": "0x60",
            "Arg": "0x21"
          }
        }
      ]
    },
    {
      "Model": "Y25f",
      "SyncType": "Free-Sync",
      "SizeX": 25
    },
    {
      "Model": "Y25g",
      "SyncType": "G-Sync",
      "SizeX": 25
    },
    {
      "Model": "Y27f",
      "SyncType": "Free-Sync",
      "SizeX": 27
    },
    {
      "Model": "Y27g",
      "SyncType": "G-Sync",
      "SizeX": 27
    },
    {
      "Model": "Y27q-20 % LEN Y27q-20",
      "SyncType": "Free-Sync",
      "SizeX": 27
    },
    {
      "Model": "Y25-25",
      "SyncType": "Free-Sync",
      "SizeX": 25
    }
  ]
}
```
