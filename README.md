# powerline_extended_cwd

This is a [powerline](https://github.com/powerline/powerline) extension that significantly enhances the cwd segment adding the ability to combine the common directory into a shortcut (i.e. "/home/username/build" -> "b"). It also adds the xterm window name support.

## Installation

```
pip install https://github.com/riarheos/powerline_extended_cwd/archive/master.zip
```

Then you must enable it in the config:
```
.config/powerline/themes/shell/default.json:
{
  "segments": {
      "left": [
                  ...
                  {
                      "function": "powerline_extended_cwd.cwd.cwd",
                      "priority": 50
                  },
                  ...
               ]
   },
   "segment_data": {
       "cwd": {
           "args": {
               "shrink": [
                   ["~/build", "b"]
               ]
           }
       }
    }
}

.config/powerline/colorschemes/default.json:
{
  "groups": {
    "cwd:home":                  { "fg": "gray6",           "bg": "gray2", "attrs": [] },
    "cwd:split":                 { "fg": "white",           "bg": "gray2", "attrs": [] }
  }
}
```
