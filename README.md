Log4j-Sublime
=============
Sublime plugin and syntax highlighting! Be gentle! Python amateur.

![](https://raw.github.com/scarrillo/Log4j-Sublime/master/imgs/log4j.png)

##### Setup:

  1: Log4j Syntax highlighting:

    - Log4j.tmLanguage - Compiled

    Install to: 
      - OSX: /Users/_user_/Library/Application Support/Sublime Text 2/Packages/User

    - Log4j.JSON-tmLanguage - Source File, not needed for installation! 

  2: Log4j Theme. Add the relevant lines to your current theme and customize!

    - log4j.tmTheme

  3: Log4j Sublime Plugin:

    - log4j.py
    - tail.py
      ** This plugin requires Kasum's awesome Python tail script.
      ** His original code is here: https://github.com/kasun/python-tail
      It's bundled here as it has some small modifications that were required in order to stop it within a thread. Many thanks!

    Install these to: 
      - OSX: /Users/_user_/Library/Application Support/Sublime Text 2/Packages/User

  4: Example key bindings:

    - Start log4j, specify a filter. Hint: debug
      { "keys": ["super+shift+t"], "command": "log4j" }

    - Bring the log4j panel to the front
      { "keys": ["ctrl+super+t"], "command": "show_panel", "args": {"panel": "output.log4j"} },

  5: Log4j: Matches with this FileAppender config

    log4j.appender.ToFile=org.apache.log4j.FileAppender
    log4j.appender.ToFile.threshold=DEBUG
    log4j.appender.ToFile.Append=false
    log4j.appender.ToFile.ImmediateFlush=true
    log4j.appender.ToFile.File=log4j.log
    log4j.appender.ToFile.layout=org.apache.log4j.PatternLayout
    log4j.appender.ToFile.layout.ConversionPattern=[%p][%c{2}]: %m%n

    - Expected output:
      [LEVEL][category]: Message


TODO:
  - Separate configuration for log file. Currently looks for: log4j.log
  - Regexp for filter
  - Optimize append. Has to be a cleaner way to open/configure/append this.
  - Figure out how to bundle this all up
  - Learn more Python oO

  
